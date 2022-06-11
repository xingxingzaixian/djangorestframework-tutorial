from rest_framework import serializers


class AuthenticationFailedSerializer(serializers.Serializer):
    detail = serializers.CharField(max_length=64)
    