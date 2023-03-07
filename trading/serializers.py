from rest_framework import serializers

from trading.models import Profile, Offer


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
