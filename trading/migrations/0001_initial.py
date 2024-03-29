# Generated by Django 3.2.17 on 2023-02-15 12:29

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cars', '0004_auto_20230213_1336'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=9, validators=[django.core.validators.MinValueValidator(0)])),
                ('birth_date', models.DateField(blank=True)),
                ('phone', models.PositiveIntegerField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SaloonToBuyerHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('deal_price', models.DecimalField(decimal_places=2, max_digits=9, validators=[django.core.validators.MinValueValidator(0)])),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sold_by_saloon', to='cars.auto')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars_bought', to='trading.profile')),
                ('saloon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars_sold_by_saloon', to='cars.autosaloon')),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('max_price', models.DecimalField(decimal_places=2, max_digits=9, validators=[django.core.validators.MinValueValidator(0)])),
                ('car_model', models.CharField(max_length=50)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='trading.profile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DealerToSaloonHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('deal_price', models.DecimalField(decimal_places=2, max_digits=9, validators=[django.core.validators.MinValueValidator(0)])),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sold_by_dealer', to='cars.auto')),
                ('dealer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars_sold_by_dealer', to='cars.dealer')),
                ('saloon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars_bought_by_saloon', to='cars.autosaloon')),
            ],
        ),
    ]
