from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Outflows
from .forms import OutflowForm
from products.models import Product

def outflow_list(request):
    outflows = Outflows.objects.all().order_by('-created_at')
    
    # Filtros
    product = request.GET.get('product')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if product:
        outflows = outflows.filter(product__id=product)
    
    if date_from:
        outflows = outflows.filter(created_at__gte=date_from)
    
    if date_to:
        outflows = outflows.filter(created_at__lte=date_to)
    
    context = {
        'outflows': outflows,
        'products': Product.objects.all(),
    }
    return render(request, 'outflows/outflow_list.html', context)

def outflow_create(request):
    if request.method == 'POST':
        form = OutflowForm(request.POST)
        if form.is_valid():
            outflow = form.save()
            messages.success(request, 'Saída de produto registrada com sucesso!')
            return redirect('outflow:outflow_list')
    else:
        form = OutflowForm()
    
    context = {
        'form': form,
        'title': 'Nova Saída de Produto',
    }
    return render(request, 'outflows/outflow_form.html', context)

def outflow_edit(request, pk):
    outflow = get_object_or_404(Outflows, pk=pk)
    
    # Guardar quantidade original para ajuste de estoque
    original_quantity = outflow.quantity
    
    if request.method == 'POST':
        form = OutflowForm(request.POST, instance=outflow)
        if form.is_valid():
            # Ajustar estoque manualmente para refletir a alteração
            product = outflow.product
            new_quantity = form.cleaned_data['quantity']
            
            # Adicionar quantidade original e remover nova quantidade
            product.quantity = product.quantity + original_quantity - new_quantity
            
            # Verificar se há estoque suficiente
            if product.quantity < 0:
                messages.error(request, f'Estoque insuficiente! Disponível: {product.quantity + new_quantity}')
                return render(request, 'outflows/outflow_form.html', {
                    'form': form,
                    'outflow': outflow,
                    'title': 'Editar Saída de Produto',
                })
            
            product.save()
            
            # Salvar sem chamar o método save do form para evitar dupla atualização
            outflow = form.save(commit=False)
            outflow.save()
            
            messages.success(request, 'Saída de produto atualizada com sucesso!')
            return redirect('outflow:outflow_list')
    else:
        form = OutflowForm(instance=outflow)
    
    context = {
        'form': form,
        'outflow': outflow,
        'title': 'Editar Saída de Produto',
    }
    return render(request, 'outflows/outflow_form.html', context)

def outflow_delete(request, pk):
    outflow = get_object_or_404(Outflows, pk=pk)
    
    if request.method == 'POST':
        # A atualização do estoque é feita pelo signal post_delete
        outflow.delete()
        messages.success(request, 'Saída de produto excluída com sucesso!')
        return redirect('outflow:outflow_list')
    
    context = {
        'outflow': outflow,
    }
    return render(request, 'outflows/outflow_confirm_delete.html', context)
