from decimal import Decimal

from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from cars.permissions import IsOwner
from cars.models import Dealer
from trading.models import Profile, Offer, DealerDiscount
from trading.serializers import ProfileSerializer, OfferSerializer, PostDealerDiscountSerializer, GetDealerDiscountSerializer
from trading.tasks import process_offer


# Create your views here.
class ProfileViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,
	mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin):

	permission_classes = [permissions.IsAuthenticated]
	serializer_class = ProfileSerializer
	
	def get_queryset(self):
		return Profile.objects.filter(user=self.request.user)
		
	def list(self, request):
		queryset = Profile.objects.all()
		profile = get_object_or_404(queryset, user=request.user)
		serializer = ProfileSerializer(profile)
		return Response(serializer.data)
		
	def perform_create(self, serializer):
		user = self.request.user
		try:
			return serializer.save(user=self.request.user, balance=Decimal(0))
		except:
			raise ValidationError("Profile already exists!")
		
		
class OfferViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
	
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = OfferSerializer
	queryset = Offer.objects.all()
	
	def perform_create(self, serializer):
		profile = self.request.user.profile
		try:
			offer = serializer.save(profile=profile)
			try:
				process_offer.delay(offer.id)
			except:
				process_offer(offer.id)
			return Response(serializer.data)
		except:
			raise ValidationError("Low balance!")


class DealerDiscountViewSet(viewsets.ModelViewSet):
	
	permission_classes = [permissions.IsAuthenticated, IsOwner]
	serializer_class = PostDealerDiscountSerializer
	queryset = DealerDiscount.objects.all()

	def list(self, request):
		discounts = DealerDiscount.objects.filter(seller__admin=request.user)
		serializer = GetDealerDiscountSerializer(discounts, many=True)
		return Response(serializer.data)

	def retrieve(self, request, pk):
		discount = get_object_or_404(DealerDiscount, pk=pk)
		serializer = GetDealerDiscountSerializer(discount)
		return Response(serializer.data)

	def perform_create(self, serializer):
		dealer = self.request.user.dealer_inst.first()
		serializer.save(seller=dealer)
		return Response(serializer.data)

