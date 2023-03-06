import datetime
from decimal import Decimal
import pytest
import pytz

from cars.models import Dealer, DealerCars, AutoSaloon, SaloonCars
from trading.models import SaloonToBuyerHistory, DealerToSaloonHistory, Offer, Profile
from trading.trading_logic import cars_by_popularity, look_for_better_discounts, saloon_buys_update_db, saloon_buys_car, find_best_offer, customer_buys_update_db, customer_buys_car

utc = pytz.UTC

@pytest.mark.parametrize(
	"hist_rec, validity",
	[
		({"A": 1, "C": 4}, 'CA'),
		({"B": 4, "C": 2, "A": 1}, 'BCA'),
		({"B": 3}, 'B'),
		({}, ''),			# no cars sold yet
	],)
@pytest.mark.django_db
def test_cars_by_popularity(cars_by_popularity_setup,saloontobuyerhistory_factory, hist_rec, validity):
	saloon, profile, cars_dict = cars_by_popularity_setup
	
	for key, value in hist_rec.items():
		for _ in range(value):
			saloontobuyerhistory_factory(
				saloon = saloon,
				profile = profile, 
				car = cars_dict[key]
			)
			
	cars_with_history = len(hist_rec)
	valid_result = [cars_dict[item].id for item in validity]
	result = cars_by_popularity(saloon)
	
	assert result[:cars_with_history] == valid_result
	assert len(result) == 3
	
	
@pytest.mark.parametrize(
	"dealer_name, discount, is_active, disc_duration, valid_dealer, valid_discounted_price",
	[
		(None, None, None, None, None, None),					# no discounts
		('A',  1.2, True, 'good', 'A', Decimal('8333.33')),		# valid discount from dealer A
		('B',  1.1, True, 'good', 'B', Decimal('9090.91')),		# valid discount from dealer B
		('C',  1.1, False, 'good', None, None),					# discount inactive
		('B',  1.1, True, 'bad', 'B', Decimal('9090.91')),		# discount time expired
	],)
@pytest.mark.django_db
def test_look_for_better_discounts(look_for_better_discounts_setup, dealerdiscount_factory, mocker, dealer_name, discount, is_active, disc_duration, valid_dealer, valid_discounted_price):
	car, saloon = look_for_better_discounts_setup
	if dealer_name:
		dealer = Dealer.objects.get(name=dealer_name)
		if disc_duration == 'good':
			start_time = utc.localize(datetime.datetime.now() - datetime.timedelta(days=1))
			end_time = utc.localize(datetime.datetime.now() + datetime.timedelta(days=1))
		else:
			start_time = utc.localize(datetime.datetime.now() - datetime.timedelta(days=2))
			end_time = utc.localize(datetime.datetime.now() - datetime.timedelta(days=1))
		disc = dealerdiscount_factory(
			seller=dealer,
			discount=float(discount),
			is_active=is_active,
			start_time = start_time,
			end_time = end_time		
			)
		disc.discounted_offers.add(dealer.cars_selling.first())
	mocker.patch("cars.utils.apply_discount", return_value=Decimal(10000))
	result = look_for_better_discounts(saloon, Decimal(10000), car)
	if result:
		assert result[0].dealer.name == valid_dealer
		assert result[1] == valid_discounted_price
	else:
		assert result == None
	
	
@pytest.mark.parametrize(
	"create_record, valid_quantity, valid_balance",
	[
		(False, 1, Decimal(490000)),		# No records in SaloonCars yet
		(True, 2, Decimal(490000))		# Car is already in saloonrecords
	],)
@pytest.mark.django_db
def test_saloon_buys_update_db(saloon_buys_update_db_setup, salooncars_factory, create_record, valid_quantity, valid_balance):
	car, dealer_rec, saloon = saloon_buys_update_db_setup
	
	saloon_balance = saloon.balance
	if create_record:
		salooncars_factory(saloon=saloon, car=car)
	saloon_rec = SaloonCars.objects.filter(saloon=saloon, car=car)
	saloon_buys_update_db(saloon, saloon_rec, dealer_rec, Decimal(10000))

	assert SaloonCars.objects.filter(saloon=saloon, car=car)[0].quantity == valid_quantity
	assert AutoSaloon.objects.last().balance == valid_balance
	assert DealerToSaloonHistory.objects.last().saloon == saloon


@pytest.mark.django_db
def test_saloon_buys_car(saloon_buys_car_setup, mocker):
	cars, saloon = saloon_buys_car_setup
	saloon_balance = saloon.balance
	print(saloon_balance)
	mocker.patch("trading.trading_logic.cars_by_popularity", return_value=cars)
	#mocker.patch("cars.utils.apply_discount", return_value=Decimal(12000))
	mocker.patch("trading.trading_logic.look_for_better_discounts", return_value=None)
	
	saloon_buys_car(saloon)
	
	assert SaloonCars.objects.filter(saloon=saloon, car__id=cars[2])[0].quantity == 1
	assert AutoSaloon.objects.last().balance == saloon_balance - Decimal(12000)
	assert DealerToSaloonHistory.objects.last().saloon == saloon
	

@pytest.mark.parametrize(
	"saloon_rec, const_disc, validity",
	[
		(False, False, None),							# no auto in saloons
		(True, False, [Decimal(15000), "sal_rec"]),		# no discounts
		(True, 3, [Decimal('12500.00'), "sal_rec"]),	# discount found
	],)
@pytest.mark.django_db
def test_find_best_offer(find_best_offer_setup, salooncars_factory, saloontobuyerhistory_factory, saloon_rec, const_disc, validity):
	offer = find_best_offer_setup
	if saloon_rec:
		rec = salooncars_factory(car=offer.car_model)
	if const_disc:
		saloon = rec.saloon
		saloon.buyer_discounts = {0: 1, 3: 1.2}
		saloon.save()
		for i in range(const_disc):
			saloontobuyerhistory_factory(saloon=saloon, profile=offer.profile, car=offer.car_model)
	
	if validity:
		validity[1] = rec
		
	result = find_best_offer(offer)

	assert result == validity
	
	
@pytest.mark.django_db	
def test_customer_buys_update_db(customer_buys_update_db_setup):
	offer, best_offer = customer_buys_update_db_setup
	saloon_balance = best_offer[1].saloon.balance
	profile_balance = offer.profile.balance
	
	customer_buys_update_db(offer, best_offer)
	
	assert SaloonCars.objects.last().quantity == 0
	assert Offer.objects.last().is_active == False
	assert AutoSaloon.objects.last().balance == saloon_balance + best_offer[0]
	assert Profile.objects.last().balance == profile_balance - best_offer[0]
	assert SaloonToBuyerHistory.objects.last().deal_price == best_offer[0]


@pytest.mark.parametrize(
	"best_offer_present, n_offers",
	[
		(None, -1),				# no dealer offers, offer deleted 
		("best_offer", 0)		# car is bought, offer inactive
	],)
@pytest.mark.django_db	
def test_customer_buys_car(customer_buys_update_db_setup, mocker, best_offer_present, n_offers):
	offer, best_offer = customer_buys_update_db_setup
	total_offers = Offer.objects.all().count()
	if best_offer_present:
		best_offer_present = best_offer
	mocker.patch("trading.trading_logic.find_best_offer", return_value=best_offer_present)
	customer_buys_car(offer)
	assert Offer.objects.all().count() == total_offers + n_offers
