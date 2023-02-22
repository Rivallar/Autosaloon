from decimal import Decimal

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

