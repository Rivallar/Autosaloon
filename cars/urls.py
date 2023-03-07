from django.urls import path, include
from rest_framework import routers

from cars.views import CarsViewSet


router = routers.DefaultRouter()
router.register('', CarsViewSet)

urlpatterns = router.urls

#urlpatterns = [
#    path('', AutoAPIView.as_view()),
#]
