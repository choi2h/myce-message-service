from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.senders.serializers import VerificationSerializer
from apps.senders.services import send_verification_email

class VerificationMailSendView(GenericAPIView):
    serializer_class = VerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        send_verification_email(serializer.validated_data)

        return Response(status=status.HTTP_200_OK)

