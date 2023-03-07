from django.urls import path, include
from rest_framework import routers

from trading.views import ProfileViewSet, OfferViewSet


router = routers.DefaultRouter()
router.register('my_profile', ProfileViewSet, basename='profile')
router.register('make_offer', OfferViewSet, basename='xxx')

urlpatterns = router.urls

#urlpatterns = [
#    path('', AutoAPIView.as_view()),
#]
