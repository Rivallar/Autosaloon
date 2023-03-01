from django.core.exceptions import ValidationError

# from trading.utils import get_auto_params


def check_characteristics_field(field_value: dict):

	"""Checks if dictionary keys are cars characteristics and their value
	types"""
	
	
	if type(field_value) is dict:
		for key, value in field_value.items():
			if not type(value) is list:
				raise ValidationError(f'"{value}" value must be a list')
			if key == 'frame':
				for item in value:
					if item not in ['bus', 'microbus', 'minivan', 'sedan', 'pickup', 'universal', 'hatchback', 'other']:
						raise ValidationError(f'Wrong value "{item}"')
			elif key == 'segment':
				for item in value:
					if item not in ['A', 'B', 'C', 'D', 'E', 'F', 'S', 'M', 'J']:
						raise ValidationError(f'Wrong value "{item}"')
			elif key == 'origin':
				for item in value:
					if item not in ['Asia', 'Europe', 'America', 'other']:
						raise ValidationError(f'Wrong value "{item}"')
			elif key == 'fuel':
				for item in value:
					if item not in ['gas', 'electro', 'petrol', 'hybrid']:
						raise ValidationError(f'Wrong value "{item}"')
			else:
				raise ValidationError(f'Wrong key "{key}"')
	else:
		raise ValidationError('Field must be a dictionary')


def check_discount_field(field_value: dict):
	
	"""Checks if dictionary keys are positive integers and values are 
	integers or float >= 1"""
	
	if type(field_value) is dict:
		for key, value in field_value.items():
			if not key.isdigit():
				raise ValidationError('Key must be positive integer')
			if not type(value) in [float, int] or value < 1:
				raise ValidationError('Value must be float >= 1')
	else:
		raise ValidationError('Field must be a dictionary')
			
