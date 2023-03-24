from decimal import Decimal
import pytest


@pytest.fixture
def setup_get_aggregated_stat(db, profile_factory, saloontobuyerhistory_factory):
	prof = profile_factory()
	empty_prof = profile_factory(user__username='empty')
	for i in 'ABCDE':
		saloontobuyerhistory_factory(profile=prof, saloon__name=i, car__model_name=i)
	saloontobuyerhistory_factory(profile=prof, deal_price=Decimal(50000), car__model_name='expensive_car')
	return prof, empty_prof


@pytest.fixture
def setup_get_dealer_stat(db, dealer_factory, autosaloon_factory, auto_factory, dealertosaloonhistory_factory):
	dealer = dealer_factory()
	empty_dealer = dealer_factory(name='empty')
	saloons = [autosaloon_factory(name=i) for i in 'ABC']
	cars = [auto_factory(model_name=i) for i in 'ZXC']

	for saloon in saloons:
		for car in cars:
			dealertosaloonhistory_factory(dealer=dealer, saloon=saloon, car=car)

	dealertosaloonhistory_factory(dealer=dealer, saloon=saloons[0], car=cars[0])
	return dealer, empty_dealer


@pytest.fixture
def setup_get_saloon_stat(db, autosaloon_factory, auto_factory, dealer_factory, profile_factory,
						  dealertosaloonhistory_factory, saloontobuyerhistory_factory):
	saloon = autosaloon_factory()
	no_hist_saloon = autosaloon_factory(name='no_hist')
	cars = [auto_factory(model_name=i) for i in 'ZXC']
	dealers = [dealer_factory(name=i) for i in 'QWE']
	profiles = [profile_factory(user__username=i) for i in 'ASD']

	for dealer in dealers:
		for car in cars:
			dealertosaloonhistory_factory(saloon=saloon, dealer=dealer, car=car)
	dealertosaloonhistory_factory(saloon=saloon, dealer=dealers[0], car=cars[0])

	for profile in profiles:
		for car in cars:
			saloontobuyerhistory_factory(saloon=saloon, profile=profile, car=car)
	saloontobuyerhistory_factory(saloon=saloon, profile=profiles[0], car=cars[0])

	return saloon, no_hist_saloon
