from django.contrib import admin

from trading.models import Profile, Offer, DealerToSaloonHistory, \
	SaloonToBuyerHistory, AutoSaloon, SaloonCars


@admin.register(DealerToSaloonHistory)
class DealerToSaloonHistoryAdmin(admin.ModelAdmin):
	list_display = ('dealer', 'saloon', 'car', 'deal_price')
	list_filter = ('dealer', 'saloon')
	
	
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'balance')
	

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
	list_display = ('profile', 'car_model', 'max_price', 'is_active')
	list_filter = ('is_active', 'car_model')


@admin.register(AutoSaloon)
class AutoSaloonAdmin(admin.ModelAdmin):
	list_display = ('name', 'balance', 'car_models_to_trade', 'car_characteristics')


@admin.register(SaloonCars)
class SaloonCarsAdmin(admin.ModelAdmin):
	list_display = ('saloon', 'car', 'quantity', 'car_price')
	list_filter = ('saloon', 'car', 'car_price')


@admin.register(SaloonToBuyerHistory)
class SaloonToBuyerHistoryAdmin(admin.ModelAdmin):
	list_display = ('saloon', 'profile', 'car', 'deal_price', 'date')
