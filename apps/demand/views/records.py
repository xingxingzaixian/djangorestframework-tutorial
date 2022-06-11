from rest_framework.viewsets import ModelViewSet

from demand.models import TblRecord
from demand.serializers import RecordSerializers


class RecordViewset(ModelViewSet):
    queryset = TblRecord.objects.all()
    serializer_class = RecordSerializers
    