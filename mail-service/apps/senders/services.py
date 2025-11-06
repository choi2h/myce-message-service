from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from apps.senders.models import get_verification_type
from apps.senders.serializers import VerificationSerializer
from apps.templates.services import build_verification_context

def send_verification_email(serializer: VerificationSerializer):
    code = serializer['code']
    type_name = serializer['verification_type']
    type_text = get_verification_type(type_name=type_name)
    context = build_verification_context(code, type_text)

    content = render_to_string(f"{context['file_name']}.html", context[
        'context'])


    send(
        to=serializer['target_email'],
        subject=context['subject'],
        content=content,
    )


def send(to: str, subject: str, content: str):
    email = EmailMultiAlternatives(
        subject=subject,
        body=content,
        from_email="noreply@myce.live",
        to=[to]
    )
    email.attach_alternative(content, "text/html")
    email.send()