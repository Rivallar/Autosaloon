from django.contrib import admin

from cars.models import Auto, Dealer, DealerCars


@admin.register(Auto)
class AutoAdmin(admin.ModelAdmin):
	list_display = ('model_name', 'vendor', 'frame', 'segment', 'origin')
	list_filter = ('vendor', 'origin', 'segment', 'frame')
	

@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
	list_display = ('name', 'cars_sold')

	
@admin.register(DealerCars)
class DealerCarsAdmin(admin.ModelAdmin):
	list_display = ('dealer', 'car', 'car_price')
	list_filter = ('dealer', 'car')



