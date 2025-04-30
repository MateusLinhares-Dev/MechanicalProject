from django.urls import path, include
from rest_framework.routers import DefaultRouter
from vehicles.views import VehicleViewSet

router = DefaultRouter()
router.register('vehicles', VehicleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
