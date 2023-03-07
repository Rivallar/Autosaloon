from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


from cars.filters import CarFilter
from cars.models import Auto
from cars.serializers import ShortAutoSerializer, FullAutoSerializer


# Create your views here.
class CarsViewSet(viewsets.ReadOnlyModelViewSet):
	
	"""List and detail views of cars, available on site"""
	
	queryset = Auto.objects.all()
	serializer_class = ShortAutoSerializer
	filter_backends = (filters.DjangoFilterBackend,)
	filterset_class = CarFilter
	
	def retrieve(self, request, pk):
		car = get_object_or_404(Auto, pk=pk)
		serializer = FullAutoSerializer(car)
		return Response(serializer.data)
