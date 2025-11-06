import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from config.exceptions import EmailSendError
from apps.senders.models import get_verification_type
from apps.senders.serializers import VerificationSerializer, \
    ConfirmReservationSerializer
import apps.templates.services as template_service
from config.exceptions import TemplateLoadError
from config.settings import EMAIL_FROM

logger = logging.getLogger(__name__)

def send_verification_email(serializer: VerificationSerializer):
    code = serializer['code']
    type_name = serializer['verification_type']
    type_text = get_verification_type(type_name=type_name)
    limit_time = serializer['limit_time']
    context = (template_service.
               build_verification_context(code, type_text, limit_time))

    content = render_html(context['file_name'], context['context'])

    send(
        to=serializer['target_email'],
        subject=context['subject'],
        content=content,
    )


def send_reservation_confirm_email(serializer: ConfirmReservationSerializer):
    context = template_service.build_reservation_confirm_context(serializer)

    content = render_html(context['file_name'], context['context'])

    send(
        to=serializer['target_email'],
        subject=context['subject'],
        content=content,
    )


def render_html(file_name: str, context: dict):
    try:
        content = render_to_string(f"{file_name}.html", context)
    except Exception as e :
        logger.error("Fail to render html. filename=%s", file_name, e)
        raise TemplateLoadError("HTML을 렌더링 할 수 없습니다.")

    return content


def send(to: str, subject: str, content: str):
    email = EmailMultiAlternatives(
        subject=subject,
        body=content,
        from_email=EMAIL_FROM,
        to=[to]
    )

    try:
        email.attach_alternative(content, "text/html")
        email.send()
    except Exception as e:
        logger.error("Fail to send email. to=%s, subject=%s", to, subject, e)
        raise EmailSendError()