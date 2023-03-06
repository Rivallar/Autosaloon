import datetime
from decimal import Decimal
from django_countries import countries
import factory
from faker import Faker
import pytz

from django.contrib.auth.models import User
from cars.models import Auto, Dealer, DealerCars, SaloonCars
from trading.models import AutoSaloon, Profile, Offer, DealerToSaloonHistory, SaloonToBuyerHistory, DealerDiscount

fake = Faker()
utc = pytz.UTC

class AutosaloonFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = AutoSaloon

    name = fake.name()
    country = countries[0]
    city = 'Minsk'
    address = 'abc'
    car_characteristics = {"origin": ["Europe"]}
    balance = Decimal(500000)


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = User

    username = fake.name()
    first_name = fake.name()


class ProfileFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    balance = Decimal(30000)


class AutoFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Auto

    model_name = fake.name()
    vendor = 'test_vendor'
    color = 'white'
    engine_volume = Decimal(2)
    transmission = 'auto'
    fuel = 'gas'
    frame = 'sedan'
    segment = 'C'
    origin = 'Europe'


class OfferFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Offer

    profile = factory.SubFactory(ProfileFactory)
    car_model = factory.SubFactory(AutoFactory)
    max_price = Decimal(25000)


class DealerFactory(factory.django.DjangoModelFactory):
	
	class Meta:
		model = Dealer
		
	name = fake.name()
	foundation_date = datetime.date.today()
	buyer_discounts = {'0': 1, '3': 1.1, '5': 1.2}
	
	
class DealercarsFactory(factory.django.DjangoModelFactory):
	
	class Meta:
		model = DealerCars
		
	dealer = factory.SubFactory(DealerFactory)
	car = factory.SubFactory(AutoFactory)
	car_price = Decimal(12000)
	
	@factory.post_generation
	def generate(self, create, extracted, **kwargs):
		if not create:
			return
		if extracted:
			if extracted == 'random':
				extracted = random.randint(2, 10)
			for _ in range(extracted):
				 DealercarsFactory(dealer=DealerFactory(name=fake.name()), car=AutoFactory(model_name='TestModel'))
				 
				 
class SalooncarsFactory(factory.django.DjangoModelFactory):
	
	class Meta:
		model = SaloonCars
		
	saloon = factory.SubFactory(AutosaloonFactory)
	car = factory.SubFactory(AutoFactory)
	quantity = 1
	car_price = Decimal(15000)
	
	
class DealertosaloonhistoryFactory(factory.django.DjangoModelFactory):
	
	class Meta:
		model = DealerToSaloonHistory

	dealer = factory.SubFactory(DealerFactory)
	saloon = factory.SubFactory(AutosaloonFactory)
	car = factory.SubFactory(AutoFactory)
	deal_price = Decimal(10000)
	

class DealerdiscountFactory(factory.django.DjangoModelFactory):

	class Meta:
		model = DealerDiscount
		
	title = fake.name()
	description = fake.text()
	discount = 1.1
	
	seller = factory.SubFactory(DealerFactory)
	start_time = utc.localize(datetime.datetime.now() - datetime.timedelta(days=1))
	end_time = utc.localize(datetime.datetime.now() + datetime.timedelta(days=1))

class SaloontobuyerhistoryFactory(factory.django.DjangoModelFactory):
	
	class Meta:
		model = SaloonToBuyerHistory
		
	saloon = factory.SubFactory(AutosaloonFactory)
	profile = factory.SubFactory(ProfileFactory)
	car = factory.SubFactory(AutoFactory)
	deal_price = Decimal(10000)
