from rest_framework import serializers

from apps.templates.models import MessageTemplate

class MessageTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTemplate
        fields = '__all__'

class UpdateTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTemplate
        fields = ['name', 'subject', 'content']

