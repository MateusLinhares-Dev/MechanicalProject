from django.urls import path
from . import views

app_name = 'service'

urlpatterns = [
    # Tipos de Serviços
    path('service-types/', views.service_type_list, name='service_type_list'),
    path('service-types/create/', views.service_type_create, name='service_type_create'),
    path('service-types/<int:pk>/edit/', views.service_type_edit, name='service_type_edit'),
    path('service-types/<int:pk>/delete/', views.service_type_delete, name='service_type_delete'),
    
    # Agendamentos
    path('schedules/', views.schedule_list, name='schedule_list'),
    path('schedules/create/', views.schedule_create, name='schedule_create'),
    path('schedules/<int:pk>/', views.schedule_detail, name='schedule_detail'),
    path('schedules/<int:pk>/edit/', views.schedule_edit, name='schedule_edit'),
    path('schedules/<int:pk>/delete/', views.schedule_delete, name='schedule_delete'),
    
    # Ordens de Serviço
    path('orders/', views.service_order_list, name='service_order_list'),
    path('orders/create/', views.service_order_create, name='service_order_create'),
    path('orders/<int:pk>/', views.service_order_detail, name='service_order_detail'),
    path('orders/<int:pk>/edit/', views.service_order_edit, name='service_order_edit'),
    path('orders/<int:pk>/delete/', views.service_order_delete, name='service_order_delete'),
    path('orders/<int:pk>/add-item/', views.add_service_item, name='add_service_item'),
    path('orders/<int:pk>/add-part/', views.add_part_usage, name='add_part_usage'),
    
    # Histórico de Manutenção
    path('maintenance-history/', views.maintenance_history_list, name='maintenance_history_list'),
    path('maintenance-history/create/', views.maintenance_history_create, name='maintenance_history_create'),
    path('maintenance-history/<int:pk>/', views.maintenance_history_detail, name='maintenance_history_detail'),
    
    # Relatórios
    path('reports/', views.reports_dashboard, name='reports_dashboard'),
    path('reports/services/', views.services_report, name='services_report'),
    path('reports/parts/', views.parts_usage_report, name='parts_usage_report'),
    path('reports/vehicles/', views.vehicles_maintenance_report, name='vehicles_maintenance_report'),
]