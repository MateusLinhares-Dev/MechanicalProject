from core.permissions import CustomDjangoModelPermission
from rest_framework import viewsets

from outflows.models import Outflows
from outflows.serializers import OutflowSerializer

class OutflowViewSet(viewsets.ModelViewSet):
    queryset = Outflows.objects.all()
    serializer_class = OutflowSerializer
    permission_classes = [CustomDjangoModelPermission]