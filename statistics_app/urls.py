from rest_framework import routers

from statistics_app.views import AutoSaloonStatisticsViewSet, DealerStatisticsViewSet, ProfileStatisticsViewSet

router = routers.DefaultRouter()

router.register('saloon', AutoSaloonStatisticsViewSet, basename='saloon_statistics')
router.register('dealer', DealerStatisticsViewSet, basename='dealer_statistics')
router.register('profile', ProfileStatisticsViewSet, basename='profile_statistics')

urlpatterns = router.urls

