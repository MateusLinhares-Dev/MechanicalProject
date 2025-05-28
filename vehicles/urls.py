from django.urls import path
from vehicles import views


app_name = 'vehicle'

urlpatterns = [
    path('vehicles_views/', views.vehicles_list_view, name='vehicles_list'),
    path('delete/<int:id>/', views.vehicle_delete_view, name='vehicle_delete'),
    path('detail/<int:id>/', views.vehicle_detail_view, name='vehicle_detail'),
    path('edit/<int:id>/', views.vehicle_edit_view, name='vehicle_edit'),
    path('create/', views.vehicle_create_view, name='vehicle_create')
]
