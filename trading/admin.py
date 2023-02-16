from django.contrib import admin

from trading.models import Profile, Offer, DealerToSaloonHistory, \
	SaloonToBuyerHistory

# Register your models here.
# admin.site.register(Profile)
# admin.site.register(Offer)
# admin.site.register(DealerToSaloonHistory)
admin.site.register(SaloonToBuyerHistory)

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
