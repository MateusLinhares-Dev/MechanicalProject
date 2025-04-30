from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet

from . import views

router = DefaultRouter()
router.register('products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('product_list/', views.product_list_view, name='product_list'),
    path('product_create/', views.product_create_view, name='product_create'),
]
