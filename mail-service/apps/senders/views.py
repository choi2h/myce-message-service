from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

import apps.senders.serializers as serializers
import apps.senders.services as send_service

class VerificationMailSendView(GenericAPIView):
    serializer_class = serializers.VerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        send_service.send_verification_email(serializer.validated_data)

        return Response(status=status.HTTP_200_OK)

class ReservationConfirmMailSendView(GenericAPIView):
    serializer_class = serializers.ConfirmReservationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        send_service.send_reservation_confirm_email(serializer.validated_data)

        return Response(status=status.HTTP_200_OK)
