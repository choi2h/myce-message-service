import json
import logging

import config.exceptions as exceptions
from apps.templates.models import MessageTemplate, MessageTemplateCode
from apps.templates.serializers import MessageTemplateSerializer, UpdateTemplateSerializer
from config.settings import SITE_URL

logger = logging.getLogger(__name__)

def update_template(template_id: int, data: UpdateTemplateSerializer):
    try :
        template = MessageTemplate.objects.get(id=template_id)
    except MessageTemplate.DoesNotExist :
        raise exceptions.TemplateNotFoundError()

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
        "site_url": SITE_URL
    })

    return template_info

def build_reservation_confirm_context(context_info):
    template_info = __get_template_info(MessageTemplateCode.RESERVATION_CONFIRM)

    template_info['context'].update({
        "name": context_info['name'],
        "expo_title": context_info['expo_title'],
        "reservation_code": context_info['reservation_code'],
        "quantity": context_info['quantity'],
        "payment_amount": context_info['payment_amount'],
        "user_type": context_info['user_type'],
        "site_url": SITE_URL
    })

    return template_info

def __get_template_info(template_code: MessageTemplateCode):
    try:
        template = MessageTemplate.objects.get(code=template_code)
    except MessageTemplate.DoesNotExist :
        logger.error("Not found template. template_code=%s", template_code)
        raise exceptions.TemplateNotFoundError()

    try:
        content = json.loads(template.content)
    except json.decoder.JSONDecodeError:
        logger.error("Fail to decode content for template. template_code=%s",
                     template_code)
        raise exceptions.TemplateLoadError()

    return {
        "file_name": template.file_name,
        "subject": template.subject,
        "context": content,
    }