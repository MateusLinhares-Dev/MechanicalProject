from django.contrib import admin
from supplier.models import Supplier

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'description','created_at', 'updated_at']
    search_fields = ['name', 'created_at']