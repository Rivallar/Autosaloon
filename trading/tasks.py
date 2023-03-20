from autosaloon.celery import app
from celery import shared_task
from cars.models import AutoSaloon
from trading.models import Offer
from trading.trading_logic import saloon_buys_car, customer_buys_car


@app.task
def saloons_are_buying():
	for saloon in AutoSaloon.objects.all():
		saloon_buys_car(saloon)
		
		
@app.task
def process_offer(offer_id):
	offer = Offer.objects.filter(id=offer_id)
	if offer:
		customer_buys_car(offer[0])
	else:
		print('Bad offer')

