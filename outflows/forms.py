from django import forms
from .models import Outflows
from products.models import Product

class OutflowForm(forms.ModelForm):
    class Meta:
        model = Outflows
        fields = ['product', 'quantity', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.filter(quantity__gt=0).order_by('name_product')
        
    def save(self, commit=True):
        outflow = super().save(commit=False)
        
        # Atualizar o estoque do produto
        product = outflow.product
        product.quantity -= outflow.quantity
        product.save()
        
        if commit:
            outflow.save()
        return outflow