from django.contrib import admin
from outflows.models import Outflows
from products.models import Product
from django.db.models import Q

@admin.register(Outflows)
class OutflowAdmin(admin.ModelAdmin):
    list_display = ['product__name_product', 'quantity', 'description', 'created_at']
    search_fields = ['quantity']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'product' and request.resolver_match.url_name.endswith('outflows_outflows_add'):
            kwargs['queryset'] = Product.objects.filter(~Q(quantity=0))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)