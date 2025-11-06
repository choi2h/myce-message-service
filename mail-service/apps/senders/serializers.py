from rest_framework import serializers


class VerificationSerializer(serializers.Serializer):
    verification_type = serializers.CharField(required=True)
    target_email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)
    limit_time = serializers.IntegerField(required=True)