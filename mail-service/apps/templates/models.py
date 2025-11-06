from django.db import models

class MessageTemplateCode(models.TextChoices):
    EMAIL_VERIFICATION = "EMAIL_VERIFICATION"
    RESET_PASSWORD = "RESET_PASSWORD"
    RESERVATION_CONFIRM = "RESERVATION_CONFIRM"


class MessageTemplate(models.Model):
    code = models.CharField(max_length=20, choices=MessageTemplateCode.choices)
    file_name = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "MessageTemplate"
        ordering = ['created_at']