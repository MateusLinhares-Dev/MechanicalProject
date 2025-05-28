from core.permissions import CustomDjangoModelPermission
from rest_framework import viewsets

from products.models import Product, ProductType
from products.serializers import ProductSerializer

from products.models import Product
from django.shortcuts import render, redirect, get_object_or_404

from products.forms import ProductForm, ProductTypeForm

from django.http import JsonResponse
from django.db.models import ProtectedError, Count


from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [CustomDjangoModelPermission]

def product_list_view(request):
    name = request.GET.get('name_product')
    brand_product = request.GET.get('brand_product')
    products = Product.objects.all()

    # Contagem de produtos com estoque baixo (quantidade <= 5)
    low_stock_count = Product.objects.filter(quantity__lte=5).count()
    
    # Contagem de categorias de produtos
    product_types_count = ProductType.objects.count()

    if (not name and not brand_product):
        context = {
            'products': products, 
            'page_title': 'Listar Produtos',
            'low_stock_count': low_stock_count,
            'product_types_count': product_types_count
        }
        return render(request, 'products/list_products.html', context)
    else:
        if name:
            products = products.filter(name_product__icontains=name)
            
        if brand_product:
            products = products.filter(product_type__name__icontains=brand_product)

        context = {
            'products': products, 
            'page_title': 'Listar Produtos',
            'low_stock_count': low_stock_count,
            'product_types_count': product_types_count,
            'name_product': name,
            'brand_product': brand_product
        }

        return render(request, 'products/list_products.html', context)

def product_create_view(request):
    if request.method == 'POST':
        new_product_form = ProductForm(request.POST)
        if new_product_form.is_valid():
            new_product_form.save()
            return redirect('product:product_list')
    else:
        new_product_form = ProductForm()

    return render(request, 'products/create_product.html', {'new_product_form': new_product_form, 'page_title':'Adicionar Novo Produto'})

def product_update(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)

        if (form.is_valid()):
            product = form.save(commit=False)
            product.product_type = form.cleaned_data['product_type']
            product.name_product = form.cleaned_data['name_product']
            product.description = form.cleaned_data['description']
            product.quantity = form.cleaned_data['quantity']

            product.save()

            return redirect('product:product_list')
        else:
            return render(request, 'products/update_product.html', {'form': form, 'product' : product, 'page_title':'Atualizar produto'})
    elif(request.method == 'GET'):
        return render(request, 'products/update_product.html', {'form': form, 'product' : product, 'page_title':'Atualizar produto'})

def product_view(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == 'GET':
        return render(request, 'products/view_product.html', {'product': product, 'page_title':'Visualizar Produto'})

def product_delete_ajax(request, id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=id)
        try:
            product.delete()
            return JsonResponse({'status': 'success', 'message': '✅ Produto apagado com sucesso.'})
        except ProtectedError:
            return JsonResponse({'status': 'error', 'message': '❌ Não é possível apagar este produto porque está relacionado com outros dados.'})
    return JsonResponse({'status': 'error', 'message': '❌ Método inválido.'})


# Views Product Type
def product_type_create_view(request):
    product_types = ProductType.objects.all()
    if request.method == 'POST':
        new_product_type_form = ProductTypeForm(request.POST)
        if new_product_type_form.is_valid():
            new_product_type_form.save()
            return redirect('product:product_list')
    else:

        new_product_type_form = ProductTypeForm()
    
    return render(request, 'products/create_product_type.html', {'new_product_type_form': new_product_type_form, 'page_title':'Adicionar tipo de produto', 'products_types': product_types})

def product_type_delete_view(request, id):
    if request.method == "POST":
        product = get_object_or_404(ProductType, pk=id)
        try:
            product.delete()
            return JsonResponse({'status': 'success', 'message': '✅ Tipo de produto apagado com sucesso.'})
        except ProtectedError:
            return JsonResponse({'status': 'error', 'message': '❌ Não é possível apagar este tipo de produto porque está relacionado com outros dados.'})
    return JsonResponse({'status': 'error', 'message': '❌ Método inválido.'})
