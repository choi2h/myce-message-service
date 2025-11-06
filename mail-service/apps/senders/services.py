import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from config.exceptions import EmailSendError
from apps.senders.models import get_verification_type
from apps.senders.serializers import VerificationSerializer, \
    ConfirmReservationSerializer, ResetPasswordSerializer
import apps.templates.services as template_service
from config.exceptions import TemplateLoadError
from config.settings import EMAIL_FROM

logger = logging.getLogger(__name__)

def send_verification_email(serializer: VerificationSerializer):
    type_name = serializer['verification_type']
    type_text = get_verification_type(type_name=type_name)

    context = (template_service.
               build_verification_context(
                    serializer['code'],
                    type_text,
                    serializer['limit_time']
                ))

    send_rendered_email(
        file_name=context['file_name'],
        subject=context['subject'],
        context=context['context'],
        to=serializer['target_email'],
    )


def send_reservation_confirm_email(serializer: ConfirmReservationSerializer):
    context = template_service.build_reservation_confirm_context(serializer)

    send_rendered_email(
        file_name=context['file_name'],
        subject=context['subject'],
        context=context['context'],
        to=serializer['target_email'],
    )

def send_reset_password_email(serializer: ResetPasswordSerializer):
    context = template_service.build_reset_password_context(serializer['temp_password'])

    send_rendered_email(
        file_name=context['file_name'],
        subject=context['subject'],
        context=context['context'],
        to=serializer['target_email'],
    )

def send_rendered_email(file_name:str, subject: str, context: dict, to: str):
    content = render_html(file_name, context)

    send(
        to=to,
        subject=subject,
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