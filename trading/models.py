from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django_countries.fields import CountryField

from cars.models import Dealer, Auto, CommonFieldsParent, DealerCars
from trading.validators import check_characteristics_field, check_discount_field
from trading.utils import find_cars_and_dealers


# Create your models here.
class Profile(CommonFieldsParent):

    """Profile of a user who wants to buy a car."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    balance = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])

    birth_date = models.DateField(blank=True, null=True)
    phone = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Offer(CommonFieldsParent):

    """An offer of a User to buy a car."""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='offers')
    max_price = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])
    car_model = models.ForeignKey(Auto, on_delete=models.CASCADE, related_name='offers')

    def clean(self):

        """Checks if max_price is lower than buyers balance."""

        if self.is_active and self.max_price > self.profile.balance:
            raise ValidationError({'max_price': 'Your balance is lower then requested price'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class AutoSaloon(CommonFieldsParent):

    """Represents all info about each auto-saloon"""

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
        self.car_models_to_trade = find_cars_and_dealers(self)
        if not self.buyer_discounts:
            self.buyer_discounts = {0: 1}
        super().save(*args, **kwargs)


class SaloonCars(models.Model):

    """Cars available in an auto-saloon"""

    saloon = models.ForeignKey(AutoSaloon, on_delete=models.CASCADE, related_name='cars_in_saloon')
    car = models.ForeignKey(Auto, on_delete=models.CASCADE, related_name='saloons_selling')

    quantity = models.PositiveSmallIntegerField(default=0)
    car_price = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])


class DealerToSaloonHistory(models.Model):

    """Dealer sells cars to Autosaloon trading history."""

    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name='cars_sold_by_dealer')
    saloon = models.ForeignKey(AutoSaloon, on_delete=models.CASCADE, related_name='cars_bought_by_saloon')
    car = models.ForeignKey(Auto, on_delete=models.CASCADE, related_name='sold_by_dealer')

    date = models.DateTimeField(auto_now_add=True)
    deal_price = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])


class SaloonToBuyerHistory(models.Model):

    """Saloon sells cars to User trading history."""

    saloon = models.ForeignKey(AutoSaloon, on_delete=models.CASCADE, related_name='cars_sold_by_saloon')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='cars_bought')
    car = models.ForeignKey(Auto, on_delete=models.CASCADE, related_name='sold_by_saloon')

    date = models.DateTimeField(auto_now_add=True)
    deal_price = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])


class DealerDiscount(CommonFieldsParent):
	
	title = models.CharField(max_length=100)
	description = models.TextField()
	discount = models.FloatField(validators=[MinValueValidator(1)])
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	
	seller = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name='discounts')
	discounted_offers = models.ManyToManyField(DealerCars, related_name='car_discount', blank=True)
	
	def clean(self):
		if self.start_time >= self.end_time:
			raise ValidationError({'end_time': 'End time must be bigger then Start time'})
			
	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)

		
	def __str__(self):
		return f'{self.seller}: {self.title}'
		

class SaloonDiscount(CommonFieldsParent):
	
	title = models.CharField(max_length=100)
	description = models.TextField()
	discount = models.FloatField(validators=[MinValueValidator(1)])
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	
	seller = models.ForeignKey(AutoSaloon, on_delete=models.CASCADE, related_name='discounts')
	discounted_offers = models.ManyToManyField(SaloonCars, related_name='car_discount', blank=True)
	
	def clean(self):
		if self.start_time >= self.end_time:
			raise ValidationError({'end_time': 'End time must be bigger then Start time'})
			
	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)

		
	def __str__(self):
		return f'{self.seller}: {self.title}'
	
