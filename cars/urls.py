from django.urls import path, include
from rest_framework import routers

from cars.views import CarsViewSet, DealerViewSet, DealerCarsViewSet, AutoSaloonViewSet, SaloonCarsViewSet


router = routers.DefaultRouter()
router.register('autos', CarsViewSet)
router.register('dealer', DealerViewSet)
router.register('dealer_cars', DealerCarsViewSet)
router.register('saloon_cars', SaloonCarsViewSet)
router.register('autosaloon', AutoSaloonViewSet)

urlpatterns = router.urls

