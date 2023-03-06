from django.db.models import Count

from datetime import datetime
from decimal import Decimal
import pytz

from cars.models import DealerCars, SaloonCars
from cars.utils import apply_discount
from trading.models import DealerToSaloonHistory, SaloonToBuyerHistory


utc = pytz.UTC


def cars_by_popularity(saloon):

    """Sorts saloon cars according to their popularity, based on trade history."""

    cars_from_history = SaloonToBuyerHistory.objects.filter(saloon=saloon).values('car').annotate(total=Count('car')).order_by('-total')
    all_saloon_cars = set(int(key) for key in saloon.car_models_to_trade.keys())
    car_priority = [item['car'] for item in cars_from_history]
    cars_never_bought = set(car_priority) ^ all_saloon_cars
    car_priority.extend(cars_never_bought)
    return car_priority
    
    
def look_for_better_discounts(saloon, const_dealer_price_discounted, car):
	
    """Checks for other dealers discounts. If a price with discount is better then from constant dealer,
    tries to buy a car from a dealer with discount."""
	
    best_price = const_dealer_price_discounted
    best_offer_rec = ''
    all_offers = DealerCars.objects.filter(car=car)
    
    curr_time = utc.localize(datetime.now())
    
    for offer in all_offers:
        discounts = offer.car_discount.filter(is_active=True, seller=offer.dealer, end_time__gt=curr_time)
        if discounts:
            final_price = apply_discount(offer.dealer, saloon, offer.car_price)
            for discount in discounts:
                final_price = final_price / Decimal(discount.discount).quantize(Decimal('0.01'))
                if final_price < best_price:
                    best_price = final_price.quantize(Decimal('0.01'))
                    best_offer_rec = offer
    if best_offer_rec:
        return (best_offer_rec, best_price)
    else:
        return None


def saloon_buys_update_db(saloon, saloon_car_record, dealer_car_record, deal_price):

    """Handles all db updates during buying from dealer process"""

    saloon_price = dealer_car_record.car_price * Decimal('1.2')
    if not saloon_car_record:
        SaloonCars.objects.create(saloon=saloon, car=dealer_car_record.car, car_price=saloon_price, quantity=1)
    else:
        saloon_car_record[0].car_price = saloon_price
        saloon_car_record[0].quantity += 1
        saloon_car_record[0].save()
    saloon.balance -= deal_price
    saloon.save()

    DealerToSaloonHistory.objects.create(dealer=dealer_car_record.dealer, saloon=saloon, car=dealer_car_record.car,
                                         deal_price=deal_price)

    message = f'Saloon {saloon.name} buys {dealer_car_record.car} from dealer {dealer_car_record.dealer}. ' \
              f'Price is {deal_price}'
    print(message)


def saloon_buys_car(saloon):

    """Saloon tries to buy a car. Loops through cars by their popularity,
    checks if there are enough such cars and if it is enough money. Updates
    db tables if car was bought."""

    cars_priority = cars_by_popularity(saloon)
    for car in cars_priority:
        #print(saloon.car_models_to_trade)
        saloon_car_record = SaloonCars.objects.filter(saloon=saloon, car=car)
        if not saloon_car_record or saloon_car_record[0].quantity < 2:
            try:
                const_dealer = saloon.car_models_to_trade[f'{car}']['dealer_id']
            except KeyError:
                const_dealer = saloon.car_models_to_trade[car]['dealer_id']
            if not const_dealer:
                print(f"Can not  buy car {car}. No one sells it.")
                break
            dealer_car_record = DealerCars.objects.get(dealer=const_dealer, car=car)
            const_dealer_price_discounted = apply_discount(dealer_car_record.dealer, saloon, dealer_car_record.car_price)
            print(f'Discounted price from a dealer: {const_dealer_price_discounted}')

            best_offer = look_for_better_discounts(saloon, const_dealer_price_discounted, car)	# checks if there are better discounts from other dealers
            if not best_offer:
                best_offer = (dealer_car_record, const_dealer_price_discounted)

            if saloon.balance >= best_offer[1]:
                saloon_buys_update_db(saloon, saloon_car_record, best_offer[0], best_offer[1])
                break
            print(f"Can not  buy car {car}. Saloon has no money.")

        else:
            print(f'Too many cars {car} in saloon')


def find_best_offer(offer):

    """Returns SaloonCars record with the lowest price."""

    saloon_records = SaloonCars.objects.filter(car=offer.car_model, quantity__gt=0, car_price__lte=offer.max_price)
    #print(f'Saloons selling {offer.car_model}: {saloon_records.values_list("saloon", "car_price")}')
    best_offer = [Decimal(999999999999), '']
    for record in saloon_records:
        n_of_deals = SaloonToBuyerHistory.objects.filter(saloon=record.saloon, profile=offer.profile).count()
        discount_options = dict(sorted(record.saloon.buyer_discounts.items()))
        discount = Decimal(1)	
        for key, value in discount_options.items():
            if n_of_deals >= int(key):
                discount = Decimal(value).quantize(Decimal('0.01'))		
                disc_price = (record.car_price / discount).quantize(Decimal('0.01'))
        curr_time = utc.localize(datetime.now())
        temp_discounts = record.car_discount.filter(is_active=True, seller=record.saloon, end_time__gt=curr_time)
        for discount in temp_discounts:
            disc_price = disc_price / Decimal(discount.discount).quantize(Decimal('0.01'))
        if disc_price < best_offer[0]:
            best_offer = [disc_price.quantize(Decimal('0.01')), record]
    print(f'Best offer is: {best_offer}')
    if best_offer[1]:
        return best_offer


def customer_buys_update_db(offer, best_offer):

    """Handles all db updates during buying from dealer process"""

    deal_price = best_offer[0]
    saloon_car = best_offer[1]

    saloon_car.quantity -= 1
    saloon_car.save()

    saloon = saloon_car.saloon
    saloon.balance += deal_price
    saloon.save()

    customer = offer.profile
    customer.balance -= deal_price
    customer.save()

    offer.is_active = False
    offer.save()

    SaloonToBuyerHistory.objects.create(saloon=saloon,
                                        profile=customer,
                                        car=offer.car_model,
                                        deal_price=deal_price)


def customer_buys_car(offer):

    """Searches for a car with the lowest price within all auto-saloons and buys it for a customer"""

    best_offer = find_best_offer(offer)

    if best_offer:
        customer_buys_update_db(offer, best_offer)
    else:
        print('Предложений, удовлетворяющих условиям не найдено')
        offer.delete(is_soft=False)
