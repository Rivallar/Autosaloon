from rest_framework import serializers

from trading.models import Profile, Offer, DealerDiscount


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Profile
		fields = ['id', 'user', 'balance', 'birth_date', 'phone']
		read_only_fields = ('user', 'balance')
		

class OfferSerializer(serializers.ModelSerializer):
	class Meta:
		model = Offer
		fields = ['profile', 'max_price', 'car_model']
		read_only_fields = ('profile',)


class DealerDiscountSerializer(serializers.ModelSerializer):
	class Meta:
		model = DealerDiscount
		fields = ['id', 'is_active', 'seller', 'title', 'description', 'discount', 'start_time', 'end_time', 'discounted_offers']
		read_only_fields = ('seller', )

