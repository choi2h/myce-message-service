from django.http import Http404

from apps.templates.models import MessageTemplate
from apps.templates.serializers import MessageTemplateSerializer, UpdateTemplateSerializer

def update_template(template_id: int, data: UpdateTemplateSerializer):
    try :
        template = MessageTemplate.objects.get(id=template_id)
    except MessageTemplate.DoesNotExist :
        raise Http404("Message Template does not exist")

    template.name = data['name']
    template.subject = data['subject']
    template.content = data['content']
    template.save()
    return MessageTemplateSerializer(template)
