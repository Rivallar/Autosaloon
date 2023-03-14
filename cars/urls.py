from django.urls import path, include
from rest_framework import routers

from cars.views import CarsViewSet, DealerViewSet, DealerCarsViewSet


router = routers.DefaultRouter()
router.register('autos', CarsViewSet)
router.register('dealer', DealerViewSet)
router.register('dealer_cars', DealerCarsViewSet)

urlpatterns = router.urls

