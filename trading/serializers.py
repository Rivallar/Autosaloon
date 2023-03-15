from rest_framework import serializers

from cars.models import DealerCars, Dealer, AutoSaloon, SaloonCars
from cars.serializers import NestedDealerSerializer, NestedDealerCarsSerializer, NestedAutoSaloonSerializer, NestedSaloonCarsSerializer
from trading.models import Profile, Offer, DealerDiscount, SaloonDiscount


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


class DealerFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
	def get_queryset(self):
		request = self.context.get('request', None)
		queryset = super().get_queryset()
		if not request or not queryset:
			return None
		dealer = Dealer.objects.get(admin=request.user)
		return queryset.filter(dealer=dealer)


class GetDealerDiscountSerializer(serializers.ModelSerializer):

	seller = NestedDealerSerializer(read_only=True)
	discounted_offers = NestedDealerCarsSerializer(many=True, read_only=True)

	class Meta:
		model = DealerDiscount
		fields = ['id', 'is_active', 'seller', 'title', 'description', 'discount', 'start_time', 'end_time', 'discounted_offers']
		read_only_fields = ('seller', )


class PostDealerDiscountSerializer(serializers.ModelSerializer):

	seller = NestedDealerSerializer(read_only=True)
	discounted_offers = DealerFilteredPrimaryKeyRelatedField(queryset=DealerCars.objects.all(), many=True)

	class Meta:
		model = DealerDiscount
		fields = ['id', 'is_active', 'seller', 'title', 'description', 'discount', 'start_time', 'end_time', 'discounted_offers']
		read_only_fields = ('seller', )


class DealerDiscountFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
	def get_queryset(self):
		request = self.context.get('request', None)
		queryset = super().get_queryset()
		if not request or not queryset:
			return None
		dealer = Dealer.objects.get(admin=request.user)
		return queryset.filter(seller=dealer)


class AttachDealerDiscountSerializer(serializers.Serializer):
	discounts = DealerDiscountFilteredPrimaryKeyRelatedField(queryset=DealerDiscount.objects.all(), many=True)


# class RemoveDealerDiscountFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
# 	def get_queryset(self):
# 		print('We are here')
# 		dealercar_pk = self.context.get('pk', None)
# 		print(self.context['request'].data)
# 		queryset = super().get_queryset()
# 		if not dealercar_pk or not queryset:
# 			return None
# 		return queryset.filter(discounted_offers__id=79)
#
#
# class RemoveDealerDiscountSerializer(serializers.Serializer):
# 	discounts = RemoveDealerDiscountFilteredPrimaryKeyRelatedField(queryset=DealerDiscount.objects.all(), many=True)


class GetSaloonDiscountSerializer(serializers.ModelSerializer):

	seller = NestedAutoSaloonSerializer(read_only=True)
	discounted_offers = NestedSaloonCarsSerializer(many=True, read_only=True)

	class Meta:
		model = SaloonDiscount
		fields = ['id', 'is_active', 'seller', 'title', 'description', 'discount', 'start_time', 'end_time', 'discounted_offers']
		read_only_fields = ('seller', )


class SaloonFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
	def get_queryset(self):
		request = self.context.get('request', None)
		queryset = super().get_queryset()
		if not request or not queryset:
			return None
		saloon = AutoSaloon.objects.get(admin=request.user)
		return queryset.filter(saloon=saloon)


class PostSaloonDiscountSerializer(serializers.ModelSerializer):

	seller = NestedAutoSaloonSerializer(read_only=True)
	discounted_offers = SaloonFilteredPrimaryKeyRelatedField(queryset=SaloonCars.objects.all(), many=True)

	class Meta:
		model = SaloonDiscount
		fields = ['id', 'is_active', 'seller', 'title', 'description', 'discount', 'start_time', 'end_time', 'discounted_offers']
		read_only_fields = ('seller', )


class SaloonDiscountFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):

	def get_queryset(self):
		print('We are here')
		request = self.context.get('request', None)
		queryset = super().get_queryset()
		if not request or not queryset:
			return None
		saloon = AutoSaloon.objects.get(admin=request.user)
		return queryset.filter(seller=saloon)


class AttachSaloonDiscountSerializer(serializers.Serializer):
	discounts = SaloonDiscountFilteredPrimaryKeyRelatedField(queryset=SaloonDiscount.objects.all(), many=True)
