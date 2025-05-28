from django.urls import path

from . import views
app_name = 'product'

urlpatterns = [
    path('product_list/', views.product_list_view, name='product_list'),
    path('product_create/', views.product_create_view, name='product_create'),
    path('product_update/<int:id>/', views.product_update, name='product_update'),
    path('product_view/<int:id>/', views.product_view, name='product_view'),
    path('products/delete_ajax/<int:id>/', views.product_delete_ajax, name='product_delete_ajax'),
    path('product_type_create/', views.product_type_create_view, name='product_type_create'),
    path('product_type_delete/<int:id>/', views.product_type_delete_view, name='product_type_delete'),
]
