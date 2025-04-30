from django.contrib import admin
from products.models import Product, ProductType

@admin.register(Product)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name_product', 'quantity', 'description','created_at', 'updated_at']
    search_fields = ['name', 'quantity', 'created_at']

@admin.register(ProductType)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'description','created_at', 'updated_at']
    search_fields = ['name', 'created_at']