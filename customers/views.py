from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Customer
from .forms import CustomerForm
from vehicles.models import Vehicle

def customer_list(request):
    customers = Customer.objects.all().order_by('name')
    
    # Filtros
    search = request.GET.get('search')
    if search:
        customers = customers.filter(name__icontains=search) | customers.filter(cpf__icontains=search)
    
    context = {
        'customers': customers,
    }
    return render(request, 'customers/customer_list.html', context)

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    vehicles = Vehicle.objects.filter(owner=customer)
    
    context = {
        'customer': customer,
        'vehicles': vehicles,
    }
    return render(request, 'customers/customer_detail.html', context)

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('customer:customer_detail', pk=customer.pk)
    else:
        form = CustomerForm()
    
    context = {
        'form': form,
        'title': 'Novo Cliente',
    }
    return render(request, 'customers/customer_form.html', context)

def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('customer:customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    
    context = {
        'form': form,
        'customer': customer,
        'title': 'Editar Cliente',
    }
    return render(request, 'customers/customer_form.html', context)

def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        try:
            customer.delete()
            messages.success(request, 'Cliente excluído com sucesso!')
            return redirect('customer:customer_list')
        except Exception as e:
            messages.error(request, f'Não foi possível excluir o cliente. Erro: {str(e)}')
            return redirect('customer:customer_detail', pk=customer.pk)
    
    context = {
        'customer': customer,
    }
    return render(request, 'customers/customer_confirm_delete.html', context)
