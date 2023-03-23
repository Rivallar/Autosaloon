from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from cars.models import AutoSaloon, Dealer
from statistics_app.stat_collectors import get_saloon_stat, get_dealer_stat, get_profile_stat
from trading.models import Profile


# Create your views here.
class AutoSaloonStatisticsViewSet(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def list(self, request):
        saloon_id = get_object_or_404(AutoSaloon, admin=request.user).id
        serializer = get_saloon_stat(saloon_id)
        if not serializer:
            raise ValidationError("Wrong statistics data!")
        return Response(serializer.data)


class DealerStatisticsViewSet(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def list(self, request):
        dealer_id = get_object_or_404(Dealer, admin=request.user).id
        serializer = get_dealer_stat(dealer_id)
        if not serializer:
            raise ValidationError("Wrong statistics data!")
        return Response(serializer.data)


class ProfileStatisticsViewSet(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (JWTAuthentication,)

    def list(self, request):
        profile_id = get_object_or_404(Profile, user=request.user).id
        serializer = get_profile_stat(profile_id)
        if not serializer:
            raise ValidationError("Wrong statistics data!")
        return Response(serializer.data)


