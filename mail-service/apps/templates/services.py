from django.http import Http404
import json

from apps.templates.models import MessageTemplate, MessageTemplateCode
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

def build_verification_context(code, type_text):
    template = MessageTemplate.objects.get(
        code=MessageTemplateCode.EMAIL_VERIFICATION)
    content = json.loads(template.content)

    context = {
        **content,
        "code":code,
        "verificationName":type_text,
        "limit_time": 10,
    }

    return {
        "file_name": template.file_name,
        "subject": template.subject,
        "context": context,
    }

