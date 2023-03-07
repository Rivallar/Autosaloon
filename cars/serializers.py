from rest_framework import serializers

from cars.models import Auto


class AutoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Auto
		fields = ['id', 'model_name', 'vendor', 'origin']
