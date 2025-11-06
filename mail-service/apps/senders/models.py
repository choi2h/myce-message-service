from django.core.exceptions import ValidationError
from django.db import models


class VerificationType(models.TextChoices):
    SIGNUP = "회원가입",
    FIND_ID = "아이디 찾기",
    FIND_PASSWORD = "비밀번호 찾기",
    NONMEMBER_VERIFY = "비회원 인증"

def get_verification_type(type_name: str):
    for v in VerificationType:
        if v.name == type_name:
            return v

    raise ValidationError(f"Invalid verification type: {type_name}")
