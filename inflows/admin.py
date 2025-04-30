from django.contrib import admin
from inflows.models import Inflows

@admin.register(Inflows)
class OutflowAdmin(admin.ModelAdmin):
    list_display = ['product__name_product', 'quantity', 'description', 'created_at']
    search_fields = ['quantity']