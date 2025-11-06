import logging
import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from config.exceptions import EmailSendError
from apps.senders.models import get_verification_type
from apps.senders.serializers import VerificationSerializer
from apps.templates.services import build_verification_context
from config.exceptions import TemplateLoadError

logger = logging.getLogger(__name__)

def send_verification_email(serializer: VerificationSerializer):
    code = serializer['code']
    type_name = serializer['verification_type']
    type_text = get_verification_type(type_name=type_name)
    limit_time = serializer['limit_time']
    context = build_verification_context(code, type_text, limit_time)

    try:
        content = render_to_string(
            f"{context['file_name']}.html",
                    context['context']
            )
    except Exception as e :
        logger.error("HTML 렌더링에 실패했습니다.", e)
        raise TemplateLoadError("HTML을 렌더링 할 수 없습니다}")

    send(
        to=serializer['target_email'],
        subject=context['subject'],
        content=content,
    )


def send(to: str, subject: str, content: str):
    email = EmailMultiAlternatives(
        subject=subject,
        body=content,
        from_email=os.getenv('FROM_EMAIL'),
        to=[to]
    )

    try:
        email.attach_alternative(content, "text/html")
        email.send()
    except Exception as e:
        logger.error("이메일 전송에 실패했습니다.", e)
        raise EmailSendError()