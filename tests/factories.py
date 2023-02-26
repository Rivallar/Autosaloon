from decimal import Decimal
from django_countries import countries
import factory
from faker import Faker

from trading.models import AutoSaloon

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

