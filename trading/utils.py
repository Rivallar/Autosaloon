from cars.models import Auto
from trading.filters import CarFilter


def find_cars_and_dealers(saloon):

    """Takes JSON-encoded set of characteristics from AutoSaloon and
    returns a dict of car models meeting these requirements with the best
    dealer to buy this car."""

    qs = Auto.objects.all()
    car_filt = saloon.car_characteristics
    cars = CarFilter(car_filt, qs).qs

    result = {}
    for car in cars:
        dealer_offers = car.dealers_selling.all().order_by('car_price')
        if dealer_offers:
            best_dealer = dealer_offers[0].dealer.name
        else:
            best_dealer = ''
        result[car.model_name] = best_dealer

    return result


# def get_auto_params(key):
#     auto_characteristics = {'frame': Auto.FrameChoices.values, 'segment': Auto.SegmentChoices.values,
#                             'origin': Auto.OriginChoices.values, 'fuel': Auto.FuelChoices.values}
#
#     return auto_characteristics[key]
