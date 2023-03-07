from rest_framework import serializers

from cars.models import Auto


class ShortAutoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Auto
		fields = ['id', 'model_name', 'vendor', 'origin']


class FullAutoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Auto
		fields = '__all__'
