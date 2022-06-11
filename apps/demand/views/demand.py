from rest_framework.viewsets import ModelViewSet

from demand.models import TblDemand
from demand.serializers import DemandSerializers


class DemandViewset(ModelViewSet):
    queryset = TblDemand.objects.all()
    serializer_class = DemandSerializers
    