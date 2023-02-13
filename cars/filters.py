import django_filters

<<<<<<< HEAD
from cars.models import Auto
=======
from .models import Auto
from .car_options_choices import FUEL_CHOICES, FRAME_CHOICES, CLASS_CHOICES, ORIGIN_CHOICES
>>>>>>> 959d07758beb37ba96c2e75229b37f2de3db3f77


class CarFilter(django_filters.FilterSet):
	
	"""Finds cars based on given specification"""
	
	origin = django_filters.MultipleChoiceFilter(choices=Auto.OriginChoices.choices)
	frame = django_filters.MultipleChoiceFilter(choices=Auto.FrameChoices.choices)
	segment = django_filters.MultipleChoiceFilter(choices=Auto.SegmentChoices.choices)
	fuel = django_filters.MultipleChoiceFilter(choices=Auto.FuelChoices.choices)
	
	class Meta:
		model = Auto
		fields = ['origin', 'frame', 'segment', 'vendor']
