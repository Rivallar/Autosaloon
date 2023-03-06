from django.urls import path
from cars.views import AutoAPIView

urlpatterns = [
    path('autos/', AutoAPIView.as_view()),
]
