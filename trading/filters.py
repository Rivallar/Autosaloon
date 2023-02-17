import django_filters

from cars.models import Auto


class CarFilter(django_filters.FilterSet):
	
	"""Finds cars based on given specification"""
	
	origin = django_filters.MultipleChoiceFilter(choices=Auto.OriginChoices.choices)
	frame = django_filters.MultipleChoiceFilter(choices=Auto.FrameChoices.choices)
	segment = django_filters.MultipleChoiceFilter(choices=Auto.SegmentChoices.choices)
	fuel = django_filters.MultipleChoiceFilter(choices=Auto.FuelChoices.choices)
	
	class Meta:
		model = Auto
		fields = ['origin', 'frame', 'segment', 'vendor']
