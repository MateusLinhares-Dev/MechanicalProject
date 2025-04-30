from django.urls import path, include
from rest_framework.routers import DefaultRouter
from outflows.views import OutflowViewSet

router = DefaultRouter()
router.register('outflows', OutflowViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
