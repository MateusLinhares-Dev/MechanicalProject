from django.urls import path, include
from rest_framework.routers import DefaultRouter
from vehicles import views

router = DefaultRouter()
router.register('vehicles_api', views.VehicleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]