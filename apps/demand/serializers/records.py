from rest_framework import serializers

from demand.models import TblRecord


class RecordSerializers(serializers.ModelSerializer):
    class Meta:
        model = TblRecord
        fields = '__all__'