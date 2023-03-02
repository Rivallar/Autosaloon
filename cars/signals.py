from django.db.models.signals import pre_save
from django.dispatch import receiver

from cars.models import AutoSaloon
from cars.utils import find_cars_and_dealers


@receiver(pre_save, sender=AutoSaloon)
def fill_car_models_to_trade_field(sender, instance, **kwargs):
    instance.car_models_to_trade = find_cars_and_dealers(instance)
