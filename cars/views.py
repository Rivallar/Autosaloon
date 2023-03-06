from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from cars.models import Auto
from cars.serializers import AutoSerializer

# Create your views here.
class AutoAPIView(generics.ListAPIView):
	
	"""Just to test JWTAuthentication."""
	
	authentication_classes = (JWTAuthentication, )
	permission_classes = (permissions.IsAuthenticated,)
	queryset = Auto.objects.all()
	serializer_class = AutoSerializer
