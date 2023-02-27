from decimal import Decimal
from django_countries import countries
import factory
from faker import Faker

from django.contrib.auth.models import User
from cars.models import Auto
from trading.models import AutoSaloon, Profile, Offer

fake = Faker()


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
    origin = 'America'


class OfferFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Offer

    profile = factory.SubFactory(Profile)
    car_model = factory.SubFactory(Auto)
    max_price = Decimal(25000)
