from rest_framework import serializers

from demand.models import TblProject


class ProjectSerializers(serializers.ModelSerializer):
    class Meta:
        model = TblProject
        fields = '__all__'