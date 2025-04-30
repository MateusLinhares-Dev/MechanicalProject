from django.contrib import admin
from vehicles.models import Vehicle, VehiclesType

@admin.register(VehiclesType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['license_plate', 'brand', 'model', 'color']
    search_fields = ['license_plate', 'brand']
    list_filter = ['vehicle_type']