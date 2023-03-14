from django.contrib.auth.models import User
from rest_framework import serializers

from cars.models import Auto, Dealer, DealerCars


class ShortAutoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Auto
		fields = ['id', 'model_name', 'vendor', 'origin']


class FullAutoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Auto
		fields = '__all__'


class NestedAutoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Auto
		fields = ['id', 'model_name']


class AdminSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'username']


class DealerSerializer(serializers.ModelSerializer):

	admin = AdminSerializer(read_only=True)

	class Meta:
		model = Dealer
		fields = ['id', 'name', 'about', 'foundation_date', 'cars_sold', 'buyer_discounts', 'admin']
		read_only_fields = ('cars_sold', 'admin')


class NestedDealerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Dealer
		fields = ['id', 'name']
		
		
class DealerCarsSerializer(serializers.ModelSerializer):
	
	discounts = serializers.SerializerMethodField()
	dealer = NestedDealerSerializer(read_only=True)
	car = NestedAutoSerializer(read_only=True)
	
	class Meta:
		model = DealerCars
		fields = ['id', 'dealer', 'car', 'car_price', 'discounts']
		read_only_fields = ('dealer', )
		
	def get_discounts(self, obj):
		return obj.car_discount.all().values_list('id', 'title', 'discount')


class PostDealerCarsSerializer(serializers.ModelSerializer):
	class Meta:
		model = DealerCars
		fields = ['id', 'dealer', 'car', 'car_price']
		read_only_fields = ('dealer', )

	def get_discounts(self, obj):
		return obj.car_discount.all().values_list('id', 'title', 'discount')


class NestedDealerCarsSerializer(serializers.ModelSerializer):

	dealer = serializers.SerializerMethodField(read_only=True)
	car = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = DealerCars
		fields = ['id', 'dealer', 'car', 'car_price']

	def get_dealer(self, obj):
		return obj.dealer.name

	def get_car(self, obj):
		return obj.car.model_name