from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Inflows
from .forms import InflowForm
from products.models import Product

def inflow_list(request):
    inflows = Inflows.objects.all().order_by('-created_at')
    
    # Filtros
    product = request.GET.get('product')
    supplier = request.GET.get('supplier')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if product:
        inflows = inflows.filter(product__id=product)
    
    if supplier:
        inflows = inflows.filter(supplier__id=supplier)
    
    if date_from:
        inflows = inflows.filter(created_at__gte=date_from)
    
    if date_to:
        inflows = inflows.filter(created_at__lte=date_to)
    
    context = {
        'inflows': inflows,
        'products': Product.objects.all(),
    }
    return render(request, 'inflows/inflow_list.html', context)

def inflow_create(request):
    if request.method == 'POST':
        form = InflowForm(request.POST)
        if form.is_valid():
            inflow = form.save()
            messages.success(request, 'Entrada de produto registrada com sucesso!')
            return redirect('inflow:inflow_list')
    else:
        form = InflowForm()
    
    context = {
        'form': form,
        'title': 'Nova Entrada de Produto',
    }
    return render(request, 'inflows/inflow_form.html', context)

def inflow_edit(request, pk):
    inflow = get_object_or_404(Inflows, pk=pk)
    
    # Guardar quantidade original para ajuste de estoque
    original_quantity = inflow.quantity
    
    if request.method == 'POST':
        form = InflowForm(request.POST, instance=inflow)
        if form.is_valid():
            # Ajustar estoque manualmente para refletir a alteração
            product = inflow.product
            new_quantity = form.cleaned_data['quantity']
            
            # Remover quantidade original e adicionar nova quantidade
            product.quantity = product.quantity - original_quantity + new_quantity
            product.save()
            
            # Salvar sem chamar o método save do form para evitar dupla atualização
            inflow = form.save(commit=False)
            inflow.save()
            
            messages.success(request, 'Entrada de produto atualizada com sucesso!')
            return redirect('inflow:inflow_list')
    else:
        form = InflowForm(instance=inflow)
    
    context = {
        'form': form,
        'inflow': inflow,
        'title': 'Editar Entrada de Produto',
    }
    return render(request, 'inflows/inflow_form.html', context)

def inflow_delete(request, pk):
    inflow = get_object_or_404(Inflows, pk=pk)
    
    if request.method == 'POST':
        # A atualização do estoque é feita pelo signal post_delete
        inflow.delete()
        messages.success(request, 'Entrada de produto excluída com sucesso!')
        return redirect('inflow:inflow_list')
    
    context = {
        'inflow': inflow,
    }
    return render(request, 'inflows/inflow_confirm_delete.html', context)
