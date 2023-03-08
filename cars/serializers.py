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


class DealerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Dealer
		fields = ['id', 'name', 'about', 'foundation_date', 'cars_sold', 'buyer_discounts', 'admin']
		read_only_fields = ('cars_sold', 'admin')
		
		
class DealerCarsSerializer(serializers.ModelSerializer):
	
	discounts = serializers.SerializerMethodField()
	
	class Meta:
		model = DealerCars
		fields = ['id', 'dealer', 'car', 'car_price', 'discounts']
		read_only_fields = ('dealer', )
		
	def get_discounts(self, obj):
		return obj.car_discount.all().values_list('id', flat=True)
