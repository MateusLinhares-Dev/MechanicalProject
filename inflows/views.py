from core.permissions import CustomDjangoModelPermission
from rest_framework import viewsets

from inflows.models import Inflows
from inflows.serializers import InflowSerializer

class InflowViewSet(viewsets.ModelViewSet):
    queryset = Inflows.objects.all()
    serializer_class = InflowSerializer
    permission_classes = [CustomDjangoModelPermission]