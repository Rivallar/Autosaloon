from decimal import Decimal
from random import shuffle

from cars.models import Auto, SaloonCars, Dealer, DealerCars
from trading.models import DealerToSaloonHistory


def cars_by_popularity(saloon):
	
	"""Sorts saloon cars according to their popularity. Currently random.""" 
	
	car_models = list(saloon.car_models_to_trade.keys())
	shuffle(car_models)
	return car_models
	
	
def update_db_after_buy(saloon, saloon_car_record, dealer_car_record):
	
	"""Handles all db updates during buying process"""
	
	saloon_price = dealer_car_record.car_price * Decimal('1.2')
	if not saloon_car_record:
		SaloonCars.objects.create(saloon=saloon, car=dealer_car_record.car,
			car_price=saloon_price, quantity=1)
	else:
		saloon_car_record[0].car_price = saloon_price
		saloon_car_record[0].quantity += 1
		saloon_car_record[0].save()
	saloon.balance -= dealer_car_record.car_price
	saloon.save()
	
	DealerToSaloonHistory.objects.create(dealer=dealer_car_record.dealer,
		saloon=saloon, car=dealer_car_record.car, deal_price=dealer_car_record.car_price)
	
	message = f'Saloon {saloon.name} buys {dealer_car_record.car} from dealer {dealer_car_record.dealer}. Price is {dealer_car_record.car_price}'
	print(message)
	
	
def saloon_buy_car(saloon):
	
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
				update_db_after_buy(saloon, saloon_car_record, dealer_car_record)
				break
			print(f"Can not  buy car {car}. Saloon has no money.")
		else:
			print(f'Too many cars {car} in saloon')

