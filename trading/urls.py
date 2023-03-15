from django.urls import path, include
from rest_framework import routers

from trading.views import ProfileViewSet, OfferViewSet, DealerDiscountViewSet, SaloonDiscountViewSet


router = routers.DefaultRouter()
router.register('my_profile', ProfileViewSet, basename='profile')
router.register('make_offer', OfferViewSet)
router.register('dealer_discounts', DealerDiscountViewSet)
router.register('saloon_discounts', SaloonDiscountViewSet)

urlpatterns = router.urls

