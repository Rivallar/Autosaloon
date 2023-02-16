from django.contrib import admin

from cars.models import Auto, AutoSaloon, SaloonCars, Dealer, DealerCars


@admin.register(Auto)
class AutoAdmin(admin.ModelAdmin):
	list_display = ('model_name', 'vendor', 'frame', 'segment',
		'origin')
	list_filter = ('vendor', 'origin', 'segment', 'frame')
	
	
@admin.register(AutoSaloon)
class AutoSaloonAdmin(admin.ModelAdmin):
	list_display = ('name', 'balance', 'car_models_to_trade',
		'car_characteristics')

		
@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
	list_display = ('name', 'cars_sold')

	
@admin.register(DealerCars)
class DealerCarsAdmin(admin.ModelAdmin):
	list_display = ('dealer', 'car', 'car_price')
	list_filter = ('dealer', 'car')


@admin.register(SaloonCars)
class SaloonCarsAdmin(admin.ModelAdmin):
	list_display = ('saloon', 'car', 'quantity', 'car_price')
	list_filter = ('saloon', 'car', 'car_price')
