from django.urls import path
from . import views

app_name = 'outflow'

urlpatterns = [
    path('', views.outflow_list, name='outflow_list'),
    path('novo/', views.outflow_create, name='outflow_create'),
    path('editar/<int:pk>/', views.outflow_edit, name='outflow_edit'),
    path('excluir/<int:pk>/', views.outflow_delete, name='outflow_delete'),
]
