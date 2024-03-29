from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from cars.models import Dealer, Auto, CommonFieldsParent, DealerCars, SoftDeleteMixin, AutoSaloon, SaloonCars


# Create your models here.
class Profile(CommonFieldsParent, SoftDeleteMixin):

    """Profile of a user who wants to buy a car."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    balance = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])

    birth_date = models.DateField(blank=True, null=True)
    phone = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Offer(CommonFieldsParent, SoftDeleteMixin):

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


class DealerDiscount(CommonFieldsParent, SoftDeleteMixin):

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


class SaloonDiscount(CommonFieldsParent, SoftDeleteMixin):

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

