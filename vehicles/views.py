from core.permissions import CustomDjangoModelPermission
from rest_framework import viewsets

from vehicles.models import Vehicle, VehiclesType, BrandTypes
from vehicles.serializers import VehicleSerializer

from django.shortcuts import render, get_object_or_404, redirect

from django.http import JsonResponse
from django.db.models import ProtectedError, Count

from vehicles.forms import VehicleForm, VehicleTypeForm

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [CustomDjangoModelPermission]

def vehicles_list_view(request):
    # Inicializa o queryset base
    vehicles_queryset = Vehicle.objects.all()
    
    # Obtém parâmetros de filtro
    search_query = request.GET.get('search', '')
    brand_filter = request.GET.get('brand', '')
    status_filter = request.GET.get('status', '')
    
    # Aplica filtros se fornecidos
    if search_query:
        vehicles_queryset = vehicles_queryset.filter(
            vehicle_name__icontains=search_query
        ) | vehicles_queryset.filter(
            license_plate__icontains=search_query
        )
    
    if brand_filter:
        vehicles_queryset = vehicles_queryset.filter(brand__id=brand_filter)
    
    if status_filter:
        vehicles_queryset = vehicles_queryset.filter(status=status_filter)
    
    # Obtém todas as marcas para o dropdown de filtro
    brands = BrandTypes.objects.all()
    
    # Contadores para os cards
    active_clients = Vehicle.objects.filter(status='ativo').count()
    in_service = Vehicle.objects.filter(status='em_servico').count()
    
    context = {
        'page_title': 'Listar Veiculos',
        'vehicles': vehicles_queryset,
        'brands': brands,
        'active_clients': active_clients,
        'in_service': in_service,
        'search_query': search_query,
        'brand_filter': brand_filter,
        'status_filter': status_filter
    }

    return render(request, 'vehicles/list_vehicles.html', context)

def vehicle_delete_view(request, id):
    if request.method == "POST":
        vehicle = get_object_or_404(Vehicle, pk=id)
        try:
            vehicle.delete()
            return JsonResponse({'status': 'success', 'message': '✅ Veiculo apagado com sucesso.'})
        except ProtectedError:
            return JsonResponse({'status': 'error', 'message': '❌ Não é possível apagar este veiculo porque está relacionado com outros dados.'})
    return JsonResponse({'status': 'error', 'message': '❌ Método inválido.'})

def vehicle_detail_view(request, id):
    vehicle = get_object_or_404(Vehicle, pk=id)

    if request.method == 'GET':
        return render(request, 'vehicles/view_vehicle.html', {'vehicle': vehicle, 'page_title':'Visualizar veiculo'})
    
def vehicle_edit_view(request, id):
    vehicle = get_object_or_404(Vehicle, pk=id)
    form = VehicleForm(instance=vehicle)
    
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)

        if (form.is_valid()):
            vehicle = form.save(commit=False)
            vehicle.vehicle_name = form.cleaned_data['vehicle_name']
            vehicle.license_plate = form.cleaned_data['license_plate']
            vehicle.brand = form.cleaned_data['brand']
            vehicle.color = form.cleaned_data['color']
            vehicle.owner = form.cleaned_data['owner']
            vehicle.vehicle_type = form.cleaned_data['vehicle_type']
            vehicle.status = form.cleaned_data.get('status', 'ativo')

            vehicle.save()

            return redirect('vehicle:vehicles_list')
        else:
            return render(request, 'vehicles/update_vehicle.html', {'form': form, 'vehicle' : vehicle, 'page_title':'Atualizar Veiculo'})
    elif(request.method == 'GET'):
        return render(request, 'vehicles/update_vehicle.html', {'form': form, 'vehicle' : vehicle, 'page_title':'Atualizar Veiculo'})
    
def vehicle_create_view(request):
    if request.method == "POST":
        print('passou aqui')
        print(request.POST)
        form = VehicleForm(request.POST)
        
        if form.is_valid():
            print('passou aqui 2')
            vehicle = form.save(commit=False)
            vehicle.status = form.cleaned_data.get('status', 'ativo')
            vehicle.save()
            return redirect('vehicle:vehicles_list')
        else:
            raise ValueError(form.errors)
    else:
        form = VehicleForm()
    return render(request, 'vehicles/create_vehicle.html', {'form':form, 'page_title':'Criar Veiculo'})
