from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from cars.models import AutoSaloon, Dealer
from statistics_app.stat_collectors import get_saloon_stat, get_dealer_stat, get_profile_stat
from trading.models import Profile


# Create your views here.
class AutoSaloonStatisticsViewSet(viewsets.ViewSet):
    def list(self, request):
        saloon_id = get_object_or_404(AutoSaloon, admin=request.user).id
        serializer = get_saloon_stat(saloon_id)
        return Response(serializer.data)


class DealerStatisticsViewSet(viewsets.ViewSet):
    def list(self, request):
        dealer_id = get_object_or_404(Dealer, admin=request.user).id
        serializer = get_dealer_stat(dealer_id)
        return Response(serializer.data)


class ProfileStatisticsViewSet(viewsets.ViewSet):
    def list(self, request):
        profile_id = get_object_or_404(Profile, user=request.user).id
        serializer = get_profile_stat(profile_id)
        return Response(serializer.data)
