from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Supplier
from .forms import SupplierForm
from inflows.models import Inflows

def supplier_list(request):
    suppliers = Supplier.objects.all().order_by('name')
    
    # Filtros
    search = request.GET.get('search')
    if search:
        suppliers = suppliers.filter(name__icontains=search)
    
    context = {
        'suppliers': suppliers,
    }
    return render(request, 'supplier/supplier_list.html', context)

def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    inflows = Inflows.objects.filter(supplier=supplier).order_by('-created_at')
    
    context = {
        'supplier': supplier,
        'inflows': inflows,
    }
    return render(request, 'supplier/supplier_detail.html', context)

def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, 'Fornecedor cadastrado com sucesso!')
            return redirect('supplier:supplier_detail', pk=supplier.pk)
    else:
        form = SupplierForm()
    
    context = {
        'form': form,
        'title': 'Novo Fornecedor',
    }
    return render(request, 'supplier/supplier_form.html', context)

def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fornecedor atualizado com sucesso!')
            return redirect('supplier:supplier_detail', pk=supplier.pk)
    else:
        form = SupplierForm(instance=supplier)
    
    context = {
        'form': form,
        'supplier': supplier,
        'title': 'Editar Fornecedor',
    }
    return render(request, 'supplier/supplier_form.html', context)

def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    
    if request.method == 'POST':
        try:
            supplier.delete()
            messages.success(request, 'Fornecedor excluído com sucesso!')
            return redirect('supplier:supplier_list')
        except Exception as e:
            messages.error(request, f'Não foi possível excluir o fornecedor. Erro: {str(e)}')
            return redirect('supplier:supplier_detail', pk=supplier.pk)
    
    context = {
        'supplier': supplier,
    }
    return render(request, 'supplier/supplier_confirm_delete.html', context)
