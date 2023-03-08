from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, mixins
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


from cars.filters import CarFilter
from cars.models import Auto, Dealer, DealerCars
from cars.permissions import IsOwner 
from cars.serializers import ShortAutoSerializer, FullAutoSerializer, DealerSerializer, DealerCarsSerializer


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


class DealerViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
	permission_classes = [permissions.IsAuthenticated, IsOwner]
	queryset = Dealer.objects.all()
	serializer_class = DealerSerializer
	
	def list(self, request):
		queryset = Dealer.objects.all()
		dealer = get_object_or_404(queryset, admin=request.user)
		serializer = DealerSerializer(dealer)
		return Response(serializer.data)
	
	
class DealerCarsViewSet(viewsets.ModelViewSet):
	permission_classes = [permissions.IsAuthenticated, IsOwner]
	queryset = DealerCars.objects.all()
	serializer_class = DealerCarsSerializer
	
	def list(self, request):
		cars = DealerCars.objects.filter(dealer__admin=request.user)
		serializer = DealerCarsSerializer(cars, many=True)
		return Response(serializer.data)

	def perform_create(self, serializer):
		dealer = self.request.user.dealer_inst.first()
		try:
			return serializer.save(dealer=dealer)
		except:
			raise ValidationError("This car is already exists for this dealer")
