from django.contrib import admin

from trading.models import Profile, Offer, DealerToSaloonHistory, \
	SaloonToBuyerHistory, AutoSaloon, SaloonCars, DealerDiscount, SaloonDiscount


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
	
	
@admin.register(DealerDiscount)
class DealerDiscountAdmin(admin.ModelAdmin):
	list_display = ('title', 'is_active', 'seller', 'discount', 'cars', 'start_time', 'end_time')
		
	def cars(self, obj):
		return list(obj.discounted_offers.all().values_list('car__model_name', flat=True))


@admin.register(SaloonDiscount)
class SaloonDiscountAdmin(admin.ModelAdmin):
	list_display = ('title', 'is_active', 'seller', 'discount', 'cars', 'start_time', 'end_time')

	def cars(self, obj):
		return list(obj.discounted_offers.all().values_list('car__model_name', flat=True))

