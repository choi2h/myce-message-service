from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response

import apps.templates.serializers as serializers
from apps.templates.service import update_template
from apps.templates.models import MessageTemplate


class TemplateView(RetrieveUpdateAPIView):
    queryset = MessageTemplate.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_serializer_class(self):
        method = self.request.method
        if method == 'PUT':
            return serializers.UpdateTemplateSerializer

        return serializers.MessageTemplateSerializer

    def put(self, request, *args, **kwargs):
        data = self.get_serializer(data=request.data)
        if not data.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        template_id = kwargs.get("id")
        template = update_template(template_id, data.validated_data)
        return Response(template.data, status=status.HTTP_200_OK)

class TemplateListView(ListAPIView):
    queryset = MessageTemplate.objects.all()
    serializer_class = serializers.MessageTemplateSerializer