from decimal import Decimal

from cars.models import Auto
from cars.filters import CarFilter
from trading.models import DealerToSaloonHistory


def apply_discount(dealer, saloon, initial_price):

    """Applies discount to a price according to the number of cars bought
    by auto-saloon from this dealer"""

    n_of_deals = DealerToSaloonHistory.objects.filter(dealer=dealer, saloon=saloon).count()
    discount_options = dict(sorted(dealer.buyer_discounts.items()))
    discount = Decimal(1)

    for key, value in discount_options.items():
        if n_of_deals >= int(key):
            discount = Decimal(value).quantize(Decimal('0.01'))

    final_price = (initial_price / discount).quantize(Decimal('0.01'))

    return final_price


def find_best_dealer(car, saloon):

    """Gets all dealer offers of a car. Loops through each offer recalculating
    the price according to discount. Returns best price with its dealer in a list"""

    dealer_offers = car.dealers_selling.all()
    best_offer = [Decimal(999999999999), '']
    for offer in dealer_offers:
        dealer = offer.dealer
        initial_price = offer.car_price
        final_price = apply_discount(dealer, saloon, initial_price)

        if final_price <= best_offer[0]:
            best_offer[0] = final_price
            best_offer[1] = dealer

    return best_offer


def find_cars_and_dealers(saloon):

    """Takes JSON-encoded set of characteristics from AutoSaloon and
    returns a dict of car models meeting these requirements with the best
    dealer to buy this car."""

    qs = Auto.objects.all()
    car_filt = saloon.car_characteristics
    cars = CarFilter(car_filt, qs).qs

    result = {}
    for car in cars:
        # dealer_offers = car.dealers_selling.all().order_by('car_price')
        dealer_offers = find_best_dealer(car, saloon)
        if dealer_offers[1]:
            best_dealer = dealer_offers[1]
            result[car.id] = {"car_model": car.model_name, "dealer_id": best_dealer.id, "dealer_name": best_dealer.name}
        else:
            result[car.id] = {"car_model": car.model_name, "dealer_id": '', "dealer_name": ''}

    return result
