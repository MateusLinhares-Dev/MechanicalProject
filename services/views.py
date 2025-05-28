from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from .models import ServiceSchedule, ServiceOrder, ServiceItem, PartUsage, MaintenanceHistory, ServiceType
from .forms import ServiceScheduleForm, ServiceOrderForm, ServiceItemForm, PartUsageForm, MaintenanceHistoryForm, ServiceTypeForm
from vehicles.models import Vehicle
from products.models import Product
from datetime import datetime

# Tipos de Serviços
def service_type_list(request):
    service_types = ServiceType.objects.all().order_by('name')
    
    # Filtro de busca
    search = request.GET.get('search')
    if search:
        service_types = service_types.filter(name__icontains=search)
    
    context = {
        'service_types': service_types,
    }
    return render(request, 'services/service_type_list.html', context)

def service_type_create(request):
    if request.method == 'POST':
        form = ServiceTypeForm(request.POST)
        if form.is_valid():
            service_type = form.save()
            messages.success(request, 'Tipo de serviço criado com sucesso!')
            return redirect('service:service_type_list')
    else:
        form = ServiceTypeForm()
    
    context = {
        'form': form,
        'title': 'Novo Tipo de Serviço',
    }
    return render(request, 'services/service_type_form.html', context)

def service_type_edit(request, pk):
    service_type = get_object_or_404(ServiceType, pk=pk)
    
    if request.method == 'POST':
        form = ServiceTypeForm(request.POST, instance=service_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tipo de serviço atualizado com sucesso!')
            return redirect('service:service_type_list')
    else:
        form = ServiceTypeForm(instance=service_type)
    
    context = {
        'form': form,
        'service_type': service_type,
        'title': 'Editar Tipo de Serviço',
    }
    return render(request, 'services/service_type_form.html', context)

def service_type_delete(request, pk):
    service_type = get_object_or_404(ServiceType, pk=pk)
    
    if request.method == 'POST':
        service_type.delete()
        messages.success(request, 'Tipo de serviço excluído com sucesso!')
        return redirect('service:service_type_list')
    
    context = {
        'service_type': service_type,
    }
    return render(request, 'services/service_type_confirm_delete.html', context)

# Agendamentos
def schedule_list(request):
    schedules = ServiceSchedule.objects.all().order_by('-scheduled_date')
    
    # Filtros
    status = request.GET.get('status')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if status:
        schedules = schedules.filter(status=status)
    
    if date_from:
        schedules = schedules.filter(scheduled_date__gte=date_from)
    
    if date_to:
        schedules = schedules.filter(scheduled_date__lte=date_to)
    
    context = {
        'schedules': schedules,
        'status_choices': ServiceSchedule.STATUS_CHOICES,
    }
    return render(request, 'services/schedule_list.html', context)

def schedule_create(request):
    param_data = request.GET.get('selected_date')
    initial = {}

    if param_data:
        try:
            data_object = datetime.strptime(param_data, "%Y-%m-%d")
            selected_datetime = data_object.replace(hour=8, minute=0)

            initial['scheduled_date'] = selected_datetime.strftime('%Y-%m-%dT%H:%M')
        except ValueError:
            pass 

    if request.method == 'POST':
        form = ServiceScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save()
            messages.success(request, 'Agendamento criado com sucesso!')
            return redirect('service:schedule_detail', pk=schedule.pk)
    else:
        form = ServiceScheduleForm(initial=initial)

    context = {
        'form': form,
        'title': 'Novo Agendamento',
    }
    return render(request, 'services/schedule_form.html', context)

def schedule_detail(request, pk):
    schedule = get_object_or_404(ServiceSchedule, pk=pk)
    context = {
        'schedule': schedule,
    }
    return render(request, 'services/schedule_detail.html', context)

def schedule_edit(request, pk):
    schedule = get_object_or_404(ServiceSchedule, pk=pk)
    
    if request.method == 'POST':
        form = ServiceScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agendamento atualizado com sucesso!')
            return redirect('service:schedule_detail', pk=schedule.pk)
    else:
        form = ServiceScheduleForm(instance=schedule)
    
    context = {
        'form': form,
        'schedule': schedule,
        'title': 'Editar Agendamento',
    }
    return render(request, 'services/schedule_form.html', context)

def schedule_delete(request, pk):
    schedule = get_object_or_404(ServiceSchedule, pk=pk)
    
    if request.method == 'POST':
        schedule.delete()
        messages.success(request, 'Agendamento excluído com sucesso!')
        return redirect('service:schedule_list')
    
    context = {
        'schedule': schedule,
    }
    return render(request, 'services/schedule_confirm_delete.html', context)

# Ordens de Serviço
def service_order_list(request):
    orders = ServiceOrder.objects.all().order_by('-created_at')
    
    # Filtros
    status = request.GET.get('status')
    vehicle = request.GET.get('vehicle')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if status:
        orders = orders.filter(status=status)
    
    if vehicle:
        orders = orders.filter(vehicle__id=vehicle)
    
    if date_from:
        orders = orders.filter(start_date__gte=date_from)
    
    if date_to:
        orders = orders.filter(start_date__lte=date_to)
    
    context = {
        'orders': orders,
        'status_choices': ServiceOrder.STATUS_CHOICES,
        'vehicles': Vehicle.objects.all(),
    }
    return render(request, 'services/service_order_list.html', context)

def service_order_create(request):
    if request.method == 'POST':
        form = ServiceOrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            messages.success(request, 'Ordem de serviço criada com sucesso!')
            return redirect('service:service_order_detail', pk=order.pk)
    else:
        # Pré-selecionar agendamento se vier da página de agendamento
        schedule_id = request.GET.get('schedule_id')
        initial = {}
        
        if schedule_id:
            try:
                schedule = ServiceSchedule.objects.get(pk=schedule_id)
                initial = {
                    'schedule': schedule,
                    'vehicle': schedule.vehicle,
                }
            except ServiceSchedule.DoesNotExist:
                pass
        
        form = ServiceOrderForm(initial=initial)
    
    context = {
        'form': form,
        'title': 'Nova Ordem de Serviço',
    }
    return render(request, 'services/service_order_form.html', context)

def service_order_detail(request, pk):
    order = get_object_or_404(ServiceOrder, pk=pk)
    service_items = order.items.all()
    parts_used = order.parts_used.all()
    
    # Calcular totais
    services_total = service_items.aggregate(total=Sum('price'))['total'] or 0
    parts_total = parts_used.aggregate(total=Sum('unit_price'))['total'] or 0
    
    context = {
        'order': order,
        'service_items': service_items,
        'parts_used': parts_used,
        'services_total': services_total,
        'parts_total': parts_total,
        'grand_total': services_total + parts_total,
    }
    return render(request, 'services/service_order_detail.html', context)

def service_order_edit(request, pk):
    order = get_object_or_404(ServiceOrder, pk=pk)
    
    if request.method == 'POST':
        form = ServiceOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ordem de serviço atualizada com sucesso!')
            return redirect('service:service_order_detail', pk=order.pk)
    else:
        form = ServiceOrderForm(instance=order)
    
    context = {
        'form': form,
        'order': order,
        'title': 'Editar Ordem de Serviço',
    }
    return render(request, 'services/service_order_form.html', context)

def service_order_delete(request, pk):
    order = get_object_or_404(ServiceOrder, pk=pk)
    
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'Ordem de serviço excluída com sucesso!')
        return redirect('service:service_order_list')
    
    context = {
        'order': order,
    }
    return render(request, 'services/service_order_confirm_delete.html', context)

def add_service_item(request, pk):
    order = get_object_or_404(ServiceOrder, pk=pk)
    
    if request.method == 'POST':
        form = ServiceItemForm(request.POST)
        if form.is_valid():
            service_item = form.save(commit=False)
            service_item.service_order = order
            service_item.save()
            
            # Atualizar o custo total da ordem de serviço
            total_services = order.items.aggregate(total=Sum('price'))['total'] or 0
            total_parts = order.parts_used.aggregate(total=Sum('unit_price'))['total'] or 0
            order.total_cost = total_services + total_parts
            order.save()
            
            messages.success(request, 'Serviço adicionado com sucesso!')
            return redirect('service:service_order_detail', pk=order.pk)
    else:
        form = ServiceItemForm()
    
    context = {
        'form': form,
        'order': order,
        'title': 'Adicionar Serviço',
    }
    return render(request, 'services/service_item_form.html', context)

def add_part_usage(request, pk):
    order = get_object_or_404(ServiceOrder, pk=pk)
    
    if request.method == 'POST':
        form = PartUsageForm(request.POST)
        if form.is_valid():
            part_usage = form.save(commit=False)
            part_usage.service_order = order
            
            # Verificar estoque
            product = part_usage.product
            if product.quantity < part_usage.quantity:
                messages.error(request, f'Estoque insuficiente! Disponível: {product.quantity}')
            else:
                # Atualizar estoque
                product.quantity -= part_usage.quantity
                product.save()
                
                part_usage.save()
                
                # Atualizar o custo total da ordem de serviço
                total_services = order.items.aggregate(total=Sum('price'))['total'] or 0
                total_parts = order.parts_used.aggregate(total=Sum('unit_price'))['total'] or 0
                order.total_cost = total_services + total_parts
                order.save()
                
                messages.success(request, 'Peça adicionada com sucesso!')
                return redirect('service:service_order_detail', pk=order.pk)
    else:
        form = PartUsageForm()
    
    context = {
        'form': form,
        'order': order,
        'title': 'Adicionar Peça',
    }
    return render(request, 'services/part_usage_form.html', context)

# Histórico de Manutenção
def maintenance_history_list(request):
    history = MaintenanceHistory.objects.all().order_by('-maintenance_date')
    
    # Filtros
    vehicle_id = request.GET.get('vehicle')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if vehicle_id:
        history = history.filter(vehicle__id=vehicle_id)
    
    if date_from:
        history = history.filter(maintenance_date__gte=date_from)
    
    if date_to:
        history = history.filter(maintenance_date__lte=date_to)
    
    context = {
        'history': history,
        'vehicles': Vehicle.objects.all(),
    }
    return render(request, 'services/maintenance_history_list.html', context)

def maintenance_history_create(request):
    if request.method == 'POST':
        form = MaintenanceHistoryForm(request.POST)
        if form.is_valid():
            history = form.save()
            messages.success(request, 'Registro de manutenção criado com sucesso!')
            return redirect('service:maintenance_history_detail', pk=history.pk)
    else:
        # Pré-selecionar veículo se vier da página de veículos
        vehicle_id = request.GET.get('vehicle_id')
        initial = {}
        
        if vehicle_id:
            try:
                vehicle = Vehicle.objects.get(pk=vehicle_id)
                initial = {'vehicle': vehicle}
            except Vehicle.DoesNotExist:
                pass
        
        form = MaintenanceHistoryForm(initial=initial)
    
    context = {
        'form': form,
        'title': 'Novo Registro de Manutenção',
    }
    return render(request, 'services/maintenance_history_form.html', context)

def maintenance_history_detail(request, pk):
    history = get_object_or_404(MaintenanceHistory, pk=pk)
    context = {
        'history': history,
    }
    return render(request, 'services/maintenance_history_detail.html', context)

# Relatórios
def reports_dashboard(request):
    # Estatísticas gerais
    total_vehicles = Vehicle.objects.count()
    total_services = ServiceOrder.objects.count()
    total_completed = ServiceOrder.objects.filter(status='concluido').count()
    total_in_progress = ServiceOrder.objects.filter(status='em_andamento').count()
    
    # Serviços por mês (últimos 6 meses)
    current_month = timezone.now().month
    current_year = timezone.now().year
    
    monthly_services = []
    for i in range(6):
        month = (current_month - i) % 12
        if month == 0:
            month = 12
        year = current_year if month <= current_month else current_year - 1
        
        count = ServiceOrder.objects.filter(
            start_date__month=month,
            start_date__year=year
        ).count()
        
        monthly_services.append({
            'month': month,
            'year': year,
            'count': count
        })
    
    # Peças mais utilizadas
    top_parts = PartUsage.objects.values(
        'product__name_product'
    ).annotate(
        total_usage=Sum('quantity')
    ).order_by('-total_usage')[:10]
    
    context = {
        'total_vehicles': total_vehicles,
        'total_services': total_services,
        'total_completed': total_completed,
        'total_in_progress': total_in_progress,
        'completion_rate': (total_completed / total_services * 100) if total_services > 0 else 0,
        'monthly_services': monthly_services,
        'top_parts': top_parts,
    }
    return render(request, 'services/reports_dashboard.html', context)

def services_report(request):
    # Filtros
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    status = request.GET.get('status')
    
    services = ServiceOrder.objects.all().order_by('-start_date')
    
    if date_from:
        services = services.filter(start_date__gte=date_from)
    
    if date_to:
        services = services.filter(start_date__lte=date_to)
    
    if status:
        services = services.filter(status=status)
    
    # Estatísticas
    total_revenue = services.aggregate(total=Sum('total_cost'))['total'] or 0
    avg_service_cost = total_revenue / services.count() if services.count() > 0 else 0
    
    context = {
        'services': services,
        'total_revenue': total_revenue,
        'avg_service_cost': avg_service_cost,
        'status_choices': ServiceOrder.STATUS_CHOICES,
    }
    return render(request, 'services/services_report.html', context)

def parts_usage_report(request):
    # Filtros
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    parts_usage = PartUsage.objects.all().order_by('-created_at')
    
    if date_from:
        parts_usage = parts_usage.filter(created_at__gte=date_from)
    
    if date_to:
        parts_usage = parts_usage.filter(created_at__lte=date_to)
    
    # Estatísticas
    total_parts_cost = parts_usage.aggregate(total=Sum('unit_price'))['total'] or 0
    parts_by_category = parts_usage.values(
        'product__product_type__name'
    ).annotate(
        count=Count('id'),
        total_cost=Sum('unit_price')
    ).order_by('-count')
    
    context = {
        'parts_usage': parts_usage,
        'total_parts_cost': total_parts_cost,
        'parts_by_category': parts_by_category,
    }
    return render(request, 'services/parts_usage_report.html', context)

def vehicles_maintenance_report(request):
    # Filtros
    vehicle_id = request.GET.get('vehicle')
    
    vehicles = Vehicle.objects.all()
    
    if vehicle_id:
        vehicles = vehicles.filter(id=vehicle_id)
    
    # Preparar dados para cada veículo
    vehicle_data = []
    for vehicle in vehicles:
        maintenance_records = MaintenanceHistory.objects.filter(vehicle=vehicle).order_by('-maintenance_date')
        service_orders = ServiceOrder.objects.filter(vehicle=vehicle).order_by('-start_date')
        
        total_maintenance_cost = service_orders.aggregate(total=Sum('total_cost'))['total'] or 0
        
        vehicle_data.append({
            'vehicle': vehicle,
            'maintenance_records': maintenance_records,
            'service_orders': service_orders,
            'total_maintenance_cost': total_maintenance_cost,
            'last_maintenance': maintenance_records.first(),
        })
    
    context = {
        'vehicle_data': vehicle_data,
        'vehicles': vehicles,
    }
    return render(request, 'services/vehicles_maintenance_report.html', context)
