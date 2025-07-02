from django.urls import path
from . import views

app_name = 'inflow'

urlpatterns = [
    path('', views.inflow_list, name='inflow_list'),
    path('novo/', views.inflow_create, name='inflow_create'),
    path('editar/<int:pk>/', views.inflow_edit, name='inflow_edit'),
    path('excluir/<int:pk>/', views.inflow_delete, name='inflow_delete'),
]