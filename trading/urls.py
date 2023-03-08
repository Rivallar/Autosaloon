from django.urls import path, include
from rest_framework import routers

from trading.views import ProfileViewSet, OfferViewSet, DealerDiscountViewSet


router = routers.DefaultRouter()
router.register('my_profile', ProfileViewSet, basename='profile')
router.register('make_offer', OfferViewSet)
router.register('discounts', DealerDiscountViewSet)

urlpatterns = router.urls

#urlpatterns = [
#    path('', AutoAPIView.as_view()),
#]
