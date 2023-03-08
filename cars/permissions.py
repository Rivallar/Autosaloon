from rest_framework import permissions


class IsOwner(permissions.BasePermission):
	
	"""Checks if current user is admin of Autosaloon or Dealer"""
	
	def has_object_permission(self, request, view, obj):
		if obj._meta.model_name == 'dealercars':
			return obj.dealer.admin == request.user
		elif obj._meta.model_name == 'salooncars':
			return obj.saloon.admin == request.user
		elif obj._meta.model_name in ('dealerdiscount', 'saloondiscount'):
			obj.seller == request.user
		else:
			return obj.admin == request.user
