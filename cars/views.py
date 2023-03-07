from django_filters import rest_framework as filters
from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication

from cars.filters import CarFilter
from cars.models import Auto
from cars.serializers import AutoSerializer


# Create your views here.
class CarsViewSet(viewsets.ReadOnlyModelViewSet):
	
	"""Just to test JWTAuthentication."""
	
	#authentication_classes = (JWTAuthentication, )
	#permission_classes = [permissions.IsAccountAdminOrReadOnly]
	queryset = Auto.objects.all()
	serializer_class = AutoSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filterset_class = CarFilter
