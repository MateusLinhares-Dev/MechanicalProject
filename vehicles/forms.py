from django import forms
from vehicles.models import Vehicle, VehiclesType

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'

class VehicleTypeForm(forms.ModelForm):
    class Meta:
        model = VehiclesType
        fields = '__all__'