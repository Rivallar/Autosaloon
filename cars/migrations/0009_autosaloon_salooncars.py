# Generated by Django 4.1.7 on 2023-02-27 12:36

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import trading.validators


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0008_alter_dealer_buyer_discounts'),
    ]

    operations = [
        migrations.CreateModel(
            name='AutoSaloon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('city', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=256)),
                ('car_characteristics', models.JSONField(default=dict, validators=[trading.validators.check_characteristics_field])),
                ('car_models_to_trade', models.JSONField(blank=True, null=True)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
                ('buyer_discounts', models.JSONField(blank=True, default=dict, null=True, validators=[trading.validators.check_discount_field])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SaloonCars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=0)),
                ('car_price', models.DecimalField(decimal_places=2, max_digits=9, validators=[django.core.validators.MinValueValidator(0)])),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saloons_selling', to='cars.auto')),
                ('saloon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars_in_saloon', to='cars.autosaloon')),
            ],
        ),
    ]
