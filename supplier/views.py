from core.permissions import CustomDjangoModelPermission
from rest_framework import viewsets

from supplier.models import Supplier
from supplier.serializers import SupplierSerializer
# Create your views here.
class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [CustomDjangoModelPermission]