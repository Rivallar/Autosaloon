from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication


from cars.filters import CarFilter
from cars.models import Auto, Dealer, DealerCars, AutoSaloon, SaloonCars
from cars.permissions import IsOwner 
from cars.serializers import ShortAutoSerializer, FullAutoSerializer, DealerSerializer, DealerCarsSerializer,\
	PostDealerCarsSerializer, AutoSaloonSerializer, SaloonCarsSerializer, PostSaloonCarsSerializer
from trading.models import DealerDiscount
from trading.serializers import AttachDealerDiscountSerializer,	AttachSaloonDiscountSerializer


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


class DealerViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
	permission_classes = [permissions.IsAuthenticated, IsOwner]
	queryset = Dealer.objects.all()
	serializer_class = DealerSerializer
	authentication_classes = (JWTAuthentication,)
	
	def list(self, request):
		queryset = Dealer.objects.all()
		dealer = get_object_or_404(queryset, admin=request.user)
		serializer = DealerSerializer(dealer)
		return Response(serializer.data)
	
	
class DealerCarsViewSet(viewsets.ModelViewSet):
	permission_classes = [permissions.IsAuthenticated, IsOwner]
	queryset = DealerCars.objects.all()
	serializer_class = DealerCarsSerializer
	authentication_classes = (JWTAuthentication,)

	def get_serializer_class(self):
		if self.action == "create":
			return PostDealerCarsSerializer
		return super().get_serializer_class()

	def list(self, request):
		cars = DealerCars.objects.filter(dealer__admin=request.user)
		serializer = DealerCarsSerializer(cars, many=True)
		return Response(serializer.data)

	def perform_create(self, serializer):
		dealer = get_object_or_404(Dealer, admin=self.request.user)
		try:
			return serializer.save(dealer=dealer)
		except:
			raise ValidationError("This car is already exists for this dealer")

	@action(detail=True, methods=['post'], serializer_class=AttachDealerDiscountSerializer)
	def add_discount(self, request, pk=None):
		car = self.get_object()
		discount_id = request.data['discounts']
		car.car_discount.add(discount_id)
		return Response(DealerCarsSerializer(car).data)

	@action(detail=True, methods=['delete'],
			url_path=r'remove_discount/(?P<discount_id>\d+)')
	def remove_discount(self, request, discount_id, pk=None):
		dealercar = get_object_or_404(DealerCars, pk=pk, dealer__admin=request.user)
		dealercar.car_discount.remove(discount_id)
		return Response(DealerCarsSerializer(dealercar).data)


class AutoSaloonViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
					mixins.DestroyModelMixin):
	permission_classes = [permissions.IsAuthenticated, IsOwner]
	queryset = AutoSaloon.objects.all()
	serializer_class = AutoSaloonSerializer
	authentication_classes = (JWTAuthentication,)

	def list(self, request):
		queryset = AutoSaloon.objects.all()
		saloon = get_object_or_404(queryset, admin=request.user)
		serializer = AutoSaloonSerializer(saloon)
		return Response(serializer.data)


class SaloonCarsViewSet(viewsets.ModelViewSet):
	permission_classes = [permissions.IsAuthenticated, IsOwner]
	queryset = SaloonCars.objects.all()
	authentication_classes = (JWTAuthentication,)

	def get_serializer_class(self):
		if self.action == "create":
			return PostSaloonCarsSerializer
		elif self.action == "add_discount":
			return AttachSaloonDiscountSerializer
		else:
			return SaloonCarsSerializer

	def list(self, request):
		cars = SaloonCars.objects.filter(saloon__admin=request.user)
		serializer = SaloonCarsSerializer(cars, many=True)
		return Response(serializer.data)

	def perform_create(self, serializer):
		saloon = get_object_or_404(AutoSaloon, admin=self.request.user)
		try:
			return serializer.save(saloon=saloon)
		except:
			raise ValidationError("This car is already exists for this autosaloon")

	@action(detail=True, methods=['post'])
	def add_discount(self, request, pk=None):
		car = self.get_object()
		discount_id = request.data['discounts']
		car.car_discount.add(discount_id)
		return Response(SaloonCarsSerializer(car).data)

	@action(detail=True, methods=['delete'],
			url_path=r'remove_discount/(?P<discount_id>\d+)')
	def remove_discount(self, request, discount_id, pk=None):
		salooncar = get_object_or_404(SaloonCars, pk=pk, saloon__admin=request.user)
		salooncar.car_discount.remove(discount_id)
		return Response(SaloonCarsSerializer(salooncar).data)
