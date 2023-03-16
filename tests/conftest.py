from decimal import Decimal
import pytest
from pytest_factoryboy import register
from django.db import connections
from rest_framework.test import APIClient, RequestsClient

from django.contrib.auth.models import User

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from tests.factories import AutosaloonFactory, ProfileFactory, AutoFactory, UserFactory, DealerFactory, \
	DealertosaloonhistoryFactory, DealercarsFactory, SaloontobuyerhistoryFactory, DealerdiscountFactory, \
	SalooncarsFactory, OfferFactory

register(AutosaloonFactory)
register(UserFactory)
register(ProfileFactory)
register(AutoFactory)
register(DealerFactory)
register(DealertosaloonhistoryFactory)
register(DealercarsFactory)
register(SaloontobuyerhistoryFactory)
register(DealerdiscountFactory)
register(SalooncarsFactory)
register(OfferFactory)

def run_sql(sql):
	conn = psycopg2.connect(database='postgres', user='Autosaloon')
	conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	cur = conn.cursor()
	cur.execute(sql)
	conn.close()
	
	
@pytest.fixture(scope='session')
def django_db_setup():
	from django.conf import settings
	
	#settings.DATABASES['default']['NAME'] = 'the_copied_db'
	
	#run_sql('DROP DATABASE IF EXISTS the_copied_db')
	#run_sql('CREATE DATABASE the_copied_db TEMPLATE postgres')
	
	#yield
	
	#for connection in connections.all():
	#	connection.close()
		
	#run_sql('DROP DATABASE the_copied_db')

	settings.DATABASES['default'] = {
		'ENGINE': 'django.db.backends.postgresql',
		'HOST': 'localhost',
		'NAME': 'postgres',
		'ATOMIC_REQUESTS': False,
	}


@pytest.fixture
def profile_and_car_for_offer(db, profile_factory, auto_factory):
	profile = profile_factory.create()
	car = auto_factory.create()
	return profile.id, car.id


@pytest.fixture
def const_discount_setup(db, auto_factory, autosaloon_factory, dealer_factory):
	car = auto_factory.create()
	saloon = autosaloon_factory.create()
	dealer = dealer_factory.create()
	return car, saloon, dealer
	

@pytest.fixture
def best_dealer_setup(db, auto_factory, autosaloon_factory):
	car = auto_factory.create()
	saloon = autosaloon_factory.create()
	return car, saloon
	
	
@pytest.fixture
def find_cars_and_dealers_setup(db, auto_factory, autosaloon_factory):
	cars = []
	for name in 'ABC':
		car = auto_factory(model_name=name)
		cars.append(car)
	saloon = autosaloon_factory()
	return saloon, cars


@pytest.fixture
def cars_by_popularity_setup(db, autosaloon_factory, auto_factory, profile_factory):
	cars_dict = {}
	for name in 'ABC':
		car = auto_factory(model_name=name)
		cars_dict[car.model_name] = car
	saloon = autosaloon_factory()
	profile = profile_factory()
	return saloon, profile, cars_dict
	
	
@pytest.fixture
def look_for_better_discounts_setup(db, auto_factory, autosaloon_factory, dealercars_factory, dealer_factory):
	car = auto_factory(model_name='TestCar')
	saloon = autosaloon_factory()
	
	for i in 'ABC':
		dealercars_factory(
			dealer = dealer_factory(name=i),
			car = car,
			car_price = Decimal(10000))
	
	return car, saloon


@pytest.fixture
def saloon_buys_update_db_setup(db, auto_factory, dealercars_factory, autosaloon_factory):
	car = auto_factory(model_name='TestCar')
	dealer_rec = dealercars_factory(car=car)
	saloon = autosaloon_factory()
	return car, dealer_rec, saloon

	
@pytest.fixture
def saloon_buys_car_setup(db, dealer_factory, auto_factory, dealercars_factory, autosaloon_factory, salooncars_factory):
	cars = []
	dealer = dealer_factory()
	for name in 'ABC':
		car = auto_factory(model_name=name)
		if name == 'A':
			car_in_saloon = car
		if name == 'B':
			dealercars_factory(car=car, dealer=dealer, car_price = Decimal(30000))
		else:
			dealercars_factory(car=car, dealer=dealer)
		cars.append(car.id)
	saloon = autosaloon_factory(balance=Decimal(20000))
	salooncars_factory(saloon=saloon, car=car_in_saloon, quantity=3)
	
	return cars, saloon


@pytest.fixture
def find_best_offer_setup(db, auto_factory, offer_factory):
	car = auto_factory()
	offer = offer_factory(car_model=car)
	return offer


@pytest.fixture
def customer_buys_update_db_setup(db, auto_factory, offer_factory, salooncars_factory):
	car = auto_factory()
	offer = offer_factory(car_model=car)
	saloon_offer = salooncars_factory(car=car)
	best_offer = [Decimal(8000), saloon_offer]
	return offer, best_offer


@pytest.fixture
def customer_buys_car_setup(db, offer_factory):
	offer = offer_factory()
	return offer


@pytest.fixture
def client():
	client
	return APIClient()
