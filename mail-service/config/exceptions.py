from rest_framework.exceptions import APIException

class TemplateNotFoundError(APIException):
    status_code = 404
    default_detail = '메시지 템플릿이 존재하지 않습니다.'
    default_code = 'TemplateNotExist'

class EmailSendError(APIException):
    status_code = 500
    default_detail = '메일 전송에 실패했습니다.'
    default_code = 'EmailSendError'

class TemplateLoadError(APIException):
    status_code = 500
    default_detail = '템플릿 형식을 로드할 수 없습니다.'
    default_code = 'TemplateLoadError'

class VerificationCoeNotFoundError(APIException):
    status_code = 400
    default_code = 'VerificationCoeNotFoundError'
    default_detail = '검증 코드가 존재하지 않습니다.'