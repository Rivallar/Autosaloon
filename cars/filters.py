import django_filters

from .models import Auto
from .car_options_choices import TRANSMISSION_CHOICES, FUEL_CHOICES, \
	FRAME_CHOICES, CLASS_CHOICES, ORIGIN_CHOICES


class CarFilter(django_filters.FilterSet):
	
	"""Finds cars based on given specification"""
	
	origin = django_filters.MultipleChoiceFilter(choices=ORIGIN_CHOICES)
	frame = django_filters.MultipleChoiceFilter(choices=FRAME_CHOICES)
	segment = django_filters.MultipleChoiceFilter(choices=CLASS_CHOICES)
	fuel = django_filters.MultipleChoiceFilter(choices=FUEL_CHOICES)
	
	class Meta:
		model = Auto
		fields = ['origin', 'frame', 'segment', 'vendor']
