from rest_framework import serializers


class VerificationSerializer(serializers.Serializer):
    verification_type = serializers.CharField(required=True)
    target_email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)
    limit_time = serializers.IntegerField(required=True)

class ConfirmReservationSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    target_email = serializers.EmailField(required=True)
    expo_title = serializers.CharField(required=True)
    reservation_code = serializers.CharField(required=True)
    quantity = serializers.IntegerField(required=True)
    payment_amount = serializers.IntegerField(required=True)
    user_type = serializers.CharField(required=True)
