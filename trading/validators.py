from django.core.exceptions import ValidationError


def check_characteristics_field(field_value: dict):
	
	"""Checks if dictionary keys are cars characteristics and their value
	types"""
	
	auto_characteristics = ['frame', 'segment', 'origin', 'fuel']
	
	if type(field_value) is dict:
		for key, value in field_value.items():
			if key in auto_characteristics:
				if not type(value) is list:
					raise ValidationError(f'"{key}" value must be a list')
			elif key == 'vendor':
				if not type(value) is str:
					raise ValidationError(f'"{key}" value must be a string')
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
			
