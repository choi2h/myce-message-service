from django.http import Http404
import json

import config.exceptions as exceptions
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

def build_verification_context(code, type_text, limit_time):
    template_info = __get_template_info(MessageTemplateCode.EMAIL_VERIFICATION)

    template_info['context'].update({
        "code":code,
        "verificationName":type_text,
        "limitTime": limit_time,
    })

    return template_info

def __get_template_info(template_code: MessageTemplateCode):
    try:
        template = MessageTemplate.objects.get(code=template_code)
    except MessageTemplate.DoesNotExist :
        raise exceptions.TemplateNotFoundError()

    try:
        content = json.loads(template.content)
    except json.decoder.JSONDecodeError:
        raise exceptions.TemplateLoadError()

    return {
        "file_name": template.file_name,
        "subject": template.subject,
        "context": content,
    }