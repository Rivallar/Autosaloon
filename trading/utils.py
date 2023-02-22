from cars.models import Auto
from trading.filters import CarFilter
# from trading.utils2 import find_best_dealer


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
		# dealer_offers = find_best_dealer(car, saloon)
		if dealer_offers:
			best_dealer = dealer_offers[1]
			result[car.model_name] = {"car_id": car.id, "dealer_id": best_dealer.id, "dealer_name": best_dealer.name}
		else:
			result[car.model_name] = {"car_id": car.id, "dealer_id": '', "dealer_name": ''}
	
	return result
