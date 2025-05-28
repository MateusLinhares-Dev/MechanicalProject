from django import forms
from .models import ServiceSchedule, ServiceOrder, ServiceItem, PartUsage, MaintenanceHistory, ServiceType
from vehicles.models import Vehicle
from products.models import Product

class ServiceTypeForm(forms.ModelForm):
    class Meta:
        model = ServiceType
        fields = ['name', 'description', 'estimated_time', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ServiceScheduleForm(forms.ModelForm):
    scheduled_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    class Meta:
        model = ServiceSchedule
        fields = ['vehicle', 'service_type', 'scheduled_date', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class ServiceOrderForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    class Meta:
        model = ServiceOrder
        fields = ['vehicle', 'schedule', 'start_date', 'status', 'diagnosis']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
        }

class ServiceItemForm(forms.ModelForm):
    class Meta:
        model = ServiceItem
        fields = ['service_type', 'description', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }

class PartUsageForm(forms.ModelForm):
    class Meta:
        model = PartUsage
        fields = ['product', 'quantity', 'unit_price']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar apenas produtos com quantidade > 0
        self.fields['product'].queryset = Product.objects.filter(quantity__gt=0)

class MaintenanceHistoryForm(forms.ModelForm):
    maintenance_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    next_maintenance_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    
    class Meta:
        model = MaintenanceHistory
        fields = ['vehicle', 'maintenance_date', 'description', 'mileage', 
                 'next_maintenance_date', 'next_maintenance_mileage']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
