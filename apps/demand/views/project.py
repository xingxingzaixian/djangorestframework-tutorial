from rest_framework.viewsets import ModelViewSet

from demand.models import TblProject
from demand.serializers import ProjectSerializers


class ProjectViewset(ModelViewSet):
    queryset = TblProject.objects.all()
    serializer_class = ProjectSerializers
    