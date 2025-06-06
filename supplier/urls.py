from django.urls import path, include
from rest_framework.routers import DefaultRouter
from supplier.views import SupplierViewSet

router = DefaultRouter()
router.register('suppliers', SupplierViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
