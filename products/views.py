from core.permissions import CustomDjangoModelPermission
from rest_framework import viewsets

from products.models import Product
from products.serializers import ProductSerializer

from products.models import Product
from django.shortcuts import render, redirect

from products.forms import ProductForm

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [CustomDjangoModelPermission]

def product_list_view(request):
    products = Product.objects.all()
    context = {'products': products, 'page_title':'Listar Produtos'}

    return render(request, 'products/list_products.html', context)

def product_create_view(request):
    if request.method == 'POST':
        new_product_form = ProductForm(request.POST)
        if new_product_form.is_valid():
            new_product_form.save()
            return redirect('product_list')
    else:
        new_product_form = ProductForm()

    return render(request, 'products/create_product.html', {'new_product_form': new_product_form, 'page_title':'Adicionar Novo Produto'})