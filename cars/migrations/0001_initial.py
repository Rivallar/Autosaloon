# Generated by Django 3.2.17 on 2023-02-08 11:25

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=100, unique=True)),
                ('vendor', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=50)),
                ('engine_volume', models.DecimalField(decimal_places=2, max_digits=4, validators=[django.core.validators.MinValueValidator(0.2), django.core.validators.MaxValueValidator(30)])),
                ('transmission', models.CharField(choices=[('mech', 'mech'), ('auto', 'auto')], default='auto', max_length=25)),
                ('fuel', models.CharField(choices=[('gas', 'gas'), ('diesel', 'diesel'), ('electro', 'electro'), ('petrol', 'petrol'), ('hybrid', 'hybrid')], default='petrol', max_length=25)),
                ('frame', models.CharField(choices=[('bus', 'bus'), ('microbus', 'microbus'), ('minivan', 'minivan'), ('sedan', 'sedan'), ('pickup', 'pickup'), ('universal', 'universal'), ('hatchback', 'hatchback'), ('other', 'other')], default='sedan', max_length=50)),
                ('segment', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('S', 'S'), ('M', 'M'), ('J', 'J')], default='C', max_length=5)),
                ('origin', models.CharField(choices=[('Asia', 'Asia'), ('Europe', 'Europe'), ('America', 'America'), ('other', 'other')], default='Europe', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='AutoSaloon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('city', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=256)),
                ('car_characteristics', models.JSONField(default={})),
                ('car_models_to_trade', models.JSONField(default=())),
                ('balance', models.DecimalField(decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
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
