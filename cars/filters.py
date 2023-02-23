import django_filters

from cars.models import Auto


class CarFilter(django_filters.FilterSet):
	
	"""Finds cars based on given specification"""
	
	origin = django_filters.CharFilter(method='filter_origin')
	frame = django_filters.MultipleChoiceFilter(choices=Auto.FrameChoices.choices)
	segment = django_filters.MultipleChoiceFilter(choices=Auto.SegmentChoices.choices)
	fuel = django_filters.MultipleChoiceFilter(choices=Auto.FuelChoices.choices)
	
	def filter_origin(self, qs, name, value):
		result = Auto.objects.none()
		print(f'Value before cycle: {value}. Its type is {type(value)}')
		for i in value:
			print(f'Current value is {i}')
			if i in ["Asia", "America", "Europe"]:
				qs = qs.filter(origin__in=value)
				print(qs)
				result = result.union(qs)
		return result
	
	class Meta:
		model = Auto
		fields = ['origin', 'frame', 'segment']
