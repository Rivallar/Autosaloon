from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models

from django_countries.fields import CountryField

from trading.validators import check_discount_field, check_characteristics_field


# Create your models here.
class Auto(models.Model):

    """Describes cars with their characteristics"""

    model_name = models.CharField(max_length=100, unique=True)
    vendor = models.CharField(max_length=100)

    color = models.CharField(max_length=50)

    engine_volume = models.DecimalField(max_digits=4, decimal_places=2,
                                        validators=[MinValueValidator(0.2), MaxValueValidator(30)])

    class TransmissionChoices(models.TextChoices):
        MECH = 'mech'
        AUTO = 'auto'

    transmission = models.CharField(max_length=25, choices=TransmissionChoices.choices, default=TransmissionChoices.AUTO)

    class FuelChoices(models.TextChoices):
        GAS = 'gas'
        DIESEL = 'diesel'
        ELECTRO = 'electro'
        PETROL = 'petrol'
        HYBRID = 'hybrid'

    fuel = models.CharField(max_length=25, choices=FuelChoices.choices, default=FuelChoices.PETROL)

    class FrameChoices(models.TextChoices):
        BUS = 'bus'
        MICROBUS = 'microbus'
        MINIVAN = 'minivan'
        SEDAN = 'sedan'
        PICKUP = 'pickup'
        UNIVERSAL = 'universal'
        HATCHBACK = 'hatchback'
        OTHER = 'other'

    frame = models.CharField(max_length=50, choices=FrameChoices.choices, default=FrameChoices.SEDAN)

    class SegmentChoices(models.TextChoices):
        A = 'A'
        B = 'B'
        C = 'C'
        D = 'D'
        E = 'E'
        F = 'F'
        S = 'S'
        M = 'M'
        J = 'J'

    segment = models.CharField(max_length=5, choices=SegmentChoices.choices, default=SegmentChoices.C)

    class OriginChoices(models.TextChoices):
        ASIA = 'Asia'
        EUROPE = 'Europe'
        AMERICA = 'America'
        OTHER = 'other'

    origin = models.CharField(max_length=50, choices=OriginChoices.choices, default=OriginChoices.EUROPE)

    def __str__(self):
        return self.model_name


class CommonFieldsParent(models.Model):

    """Abstract model to describe common fields in child-models"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
        
class SoftDeleteMixin(models.Model):

    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def delete(self, is_soft=True, *args, **kwargs):
        if is_soft:
            self.is_active = False
            self.save()
        else:
            super().delete(*args, **kwargs)


class Dealer(CommonFieldsParent, SoftDeleteMixin):

    """Represents info about car dealers"""

    admin = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='dealer_inst', blank=True, null=True)
    name = models.CharField(max_length=100, unique=True)
    about = models.TextField(blank=True)
    foundation_date = models.DateField()
    cars_sold = models.PositiveIntegerField(default=0)
    buyer_discounts = models.JSONField(default=dict, blank=True,
        null=True, validators=[check_discount_field])
    
    def save(self, *args, **kwargs):
        if not self.buyer_discounts:
            self.buyer_discounts = {0: 1}
        super().save(*args, **kwargs)	

    def __str__(self):
        return self.name


class DealerCars(models.Model):

    """Dealers cars"""

    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name='cars_selling')
    car = models.ForeignKey(Auto, on_delete=models.CASCADE, related_name='dealers_selling')
    car_price = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['dealer', 'car'], name='Must be unique'),
            ]
            
    def __str__(self):
        return f'{self.car} from {self.dealer}'


class AutoSaloon(CommonFieldsParent, SoftDeleteMixin):

    """Represents all info about each auto-saloon"""
    
    admin = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='saloon_inst', blank=True, null=True)
    name = models.CharField(max_length=100, unique=True)

    country = CountryField()
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=256)

    car_characteristics = models.JSONField(default=dict, validators=[check_characteristics_field])
    car_models_to_trade = models.JSONField(blank=True, null=True)

    balance = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    buyer_discounts = models.JSONField(default=dict, blank=True,
                                       null=True, validators=[check_discount_field])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # to form "car_models_to_trade" field
        # self.car_models_to_trade = find_cars_and_dealers(self)
        if not self.buyer_discounts:
            self.buyer_discounts = {0: 1}
        super().save(*args, **kwargs)


class SaloonCars(models.Model):
    """Cars available in an auto-saloon"""

    saloon = models.ForeignKey(AutoSaloon, on_delete=models.CASCADE, related_name='cars_in_saloon')
    car = models.ForeignKey(Auto, on_delete=models.CASCADE, related_name='saloons_selling')

    quantity = models.PositiveSmallIntegerField(default=0)
    car_price = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['saloon', 'car'], name='Must be unique record'),
            ]

    def __str__(self):
        return f'{self.car} from {self.saloon}'
