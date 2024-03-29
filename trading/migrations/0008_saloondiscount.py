# Generated by Django 3.2.18 on 2023-02-22 08:35

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0007_alter_dealerdiscount_discounted_offers'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaloonDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('discount', models.FloatField(validators=[django.core.validators.MinValueValidator(1)])),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('discounted_offers', models.ManyToManyField(blank=True, related_name='car_discount', to='trading.SaloonCars')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discounts', to='trading.autosaloon')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
