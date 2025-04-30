from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inflows.views import InflowViewSet

router = DefaultRouter()
router.register('inflows', InflowViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
