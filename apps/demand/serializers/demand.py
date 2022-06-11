from rest_framework import serializers

from demand.models import TblDemand


class DemandSerializers(serializers.ModelSerializer):
    class Meta:
        model = TblDemand
        fields = '__all__'