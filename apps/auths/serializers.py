from attr import fields
from rest_framework import serializers

from auths.models import TblRole


class RoleSerializers(serializers.ModelSerializer):
    class Meta:
        model = TblRole
        fields = '__all__'
