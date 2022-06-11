from rest_framework.viewsets import ModelViewSet

from auths.models import TblRole
from auths.serializers import RoleSerializers


class RoleViewset(ModelViewSet):
    queryset = TblRole.objects.all()
    serializer_class = RoleSerializers
    