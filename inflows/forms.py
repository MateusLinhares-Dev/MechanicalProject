from django import forms
from .models import Inflows
from products.models import Product
from supplier.models import Supplier

class InflowForm(forms.ModelForm):
    class Meta:
        model = Inflows
        fields = ['supplier', 'product', 'quantity', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['supplier'].queryset = Supplier.objects.all().order_by('name')
        self.fields['product'].queryset = Product.objects.all().order_by('name_product')
        
    def save(self, commit=True):
        inflow = super().save(commit=False)
        
        # Atualizar o estoque do produto
        product = inflow.product
        product.quantity += inflow.quantity
        product.save()
        
        if commit:
            inflow.save()
        return inflow