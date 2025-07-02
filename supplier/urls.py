from django.urls import path
from . import views

app_name = 'supplier'

urlpatterns = [
    path('', views.supplier_list, name='supplier_list'),
    path('<int:pk>/', views.supplier_detail, name='supplier_detail'),
    path('novo/', views.supplier_create, name='supplier_create'),
    path('editar/<int:pk>/', views.supplier_edit, name='supplier_edit'),
    path('excluir/<int:pk>/', views.supplier_delete, name='supplier_delete'),
]
