from decimal import Decimal
from random import shuffle

from cars.models import DealerCars
from trading.models import DealerToSaloonHistory, SaloonCars, SaloonToBuyerHistory


def cars_by_popularity(saloon):

    """Sorts saloon cars according to their popularity. Currently, random."""

    car_models = list(saloon.car_models_to_trade.keys())
    shuffle(car_models)
    return car_models


def saloon_buys_update_db(saloon, saloon_car_record, dealer_car_record):

    """Handles all db updates during buying from dealer process"""

    saloon_price = dealer_car_record.car_price * Decimal('1.2')
    if not saloon_car_record:
        SaloonCars.objects.create(saloon=saloon, car=dealer_car_record.car, car_price=saloon_price, quantity=1)
    else:
        saloon_car_record[0].car_price = saloon_price
        saloon_car_record[0].quantity += 1
        saloon_car_record[0].save()
    saloon.balance -= dealer_car_record.car_price
    saloon.save()

    DealerToSaloonHistory.objects.create(dealer=dealer_car_record.dealer, saloon=saloon, car=dealer_car_record.car,
                                         deal_price=dealer_car_record.car_price)

    message = f'Saloon {saloon.name} buys {dealer_car_record.car} from dealer {dealer_car_record.dealer}. ' \
              f'Price is {dealer_car_record.car_price}'
    print(message)


def saloon_buys_car(saloon):

    """Saloon tries to buy a car. Loops through cars by their popularity,
    checks if there are enough such cars and if it is enough money. Updates
    db tables if car was bought."""

    cars_priority = cars_by_popularity(saloon)
    for car in cars_priority:
        saloon_car_record = SaloonCars.objects.filter(saloon=saloon, car__model_name=car)
        if not saloon_car_record or saloon_car_record[0].quantity < 2:	# Only two cars in saloon to test logic
            dealer_car_record = DealerCars.objects.get(dealer__name=saloon.car_models_to_trade[car],
                                                       car__model_name=car)
            if saloon.balance >= dealer_car_record.car_price:
                saloon_buys_update_db(saloon, saloon_car_record, dealer_car_record)
                break
            print(f"Can not  buy car {car}. Saloon has no money.")
        else:
            print(f'Too many cars {car} in saloon')


def find_best_offer(offer):

    """Returns SaloonCars record with the lowest price."""

    best_offer = SaloonCars.objects.filter(car=offer.car_model, quantity__gt=0, car_price__lte=offer.max_price). \
        order_by('car_price')
    if best_offer:
        return best_offer[0]


def customer_buys_update_db(offer, best_offer):

    """Handles all db updates during buying from dealer process"""

    deal_price = best_offer.car_price

    best_offer.quantity -= 1
    best_offer.save()

    saloon = best_offer.saloon
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
        offer.delete()
