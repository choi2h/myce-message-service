# MYCE Mail Service

MYCE 플랫폼의 이메일 발송 서비스입니다. 이메일 템플릿을 관리하고, 다양한 종류의 알림 이메일을 전송합니다.

## 📋 목차

- [프로젝트 개요](#프로젝트-개요)
- [기술 스택](#기술-스택)
- [설치 및 실행](#설치-및-실행)
- [프로젝트 구조](#프로젝트-구조)
- [API 엔드포인트](#api-엔드포인트)
- [데이터베이스 스키마](#데이터베이스-스키마)
- [주요 기능](#주요-기능)


---

<br/>

## 프로젝트 개요

MYCE Mail Service는 Myce 사용자에게 다양한 이메일을 전송하는 마이크로서비스입니다.

### 주요 기능
- ✅ HTML 기반 이메일 템플릿 관리
- ✅ AWS SES SMTP를 통한 안정적인 이메일 전송
- ✅ 사용자 타입(회원/비회원)별 동적 콘텐츠
- ✅ 이메일 템플릿 CRUD API

### 지원 이메일 종류

| 코드 | 설명 |
|------|------|
| `EMAIL_VERIFICATION` | 이메일 인증 |
| `RESET_PASSWORD` | 비밀번호 재설정 |
| `RESERVATION_CONFIRM` | 예약 확인 |

<br/>

## 기술 스택

- **Framework**: Django 5.2.7
- **REST API**: Django REST Framework
- **Database**: MySQL
- **Email Service**: AWS SES SMTP
- **Python**: 3.9+

<br/>

## 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/myce/myce-mail-service.git
cd myce-mail-service/mail-service
```

### 2. 가상 환경 생성
```bash
pyenv virtualenv mms

## 가상환경 시작
pyenv activate mms
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정
```bash
vi .env
```

`.env` 파일을 편집하여 필요한 환경 변수를 설정합니다.

### 5. 데이터베이스 생성
```bash
python manage.py makemigrations

python manage.py migrate
```

### 6. 서버 실행
```bash
python manage.py runserver
```

서버는 `http://localhost:8000`에서 실행됩니다.

<br/>

## 프로젝트 구조

```
mail-service/
├── config/                          # Django 프로젝트 설정
│   ├── settings.py                  # 프로젝트 설정
│   ├── urls.py                      # URL 라우팅
│   ├── wsgi.py                      # WSGI 설정
│   ├── asgi.py                      # ASGI 설정
│   └── exceptions.py                # 공용 예외 클래스
│
├── apps/                            # Django 앱
│   ├── senders/                     # 이메일 전송 앱
│   │   ├── views.py                 # API 뷰
│   │   ├── services.py              # 비즈니스 로직
│   │   ├── serializers.py           # 데이터 직렬화
│   │   ├── models.py                # 검증 타입 정의
│   │   ├── urls.py                  # URL 라우팅
│   │   ├── exceptions.py            # 예외 클래스
│   │   └── migrations/              # DB 마이그레이션
│   │
│   └── templates/                   # 이메일 템플릿 관리 앱
│       ├── views.py                 # 템플릿 CRUD API
│       ├── services.py              # 템플릿 관련 로직
│       ├── serializers.py           # 템플릿 직렬화
│       ├── models.py                # 템플릿 모델
│       ├── urls.py                  # URL 라우팅
│       └── migrations/              # DB 마이그레이션
│
├── resources/
│   └── templates/                   # HTML 이메일 템플릿
│       ├── mail-password.html       # 비밀번호 재설정 템플릿
│       ├── mail-code.html           # 인증 코드 템플릿
│       └── mail-reservation.html    # 예약 확인 템플릿
│
├── manage.py                        # Django 관리 스크립트
├── .env                             # 환경 변수
├── .gitignore                       # Git 무시 파일
└── requirements.txt                 # Python 의존성
```

<br/>

## API 엔드포인트

### 1. 인증 이메일 전송

**POST** `/senders/verification/`

요청 본문:
```json
{
  "code": "123456",
  "verification_type": "회원가입",
  "target_email": "user@example.com",
  "limit_time": 10,
  "user_type": "MEMBER"
}
```

응답:
```json
{
  "success": true,
  "message": "인증 이메일이 성공적으로 전송되었습니다."
}
```

### 2. 예약 확인 이메일 전송

**POST** `/senders/reservation/confirm/`

요청 본문:
```json
{
  "target_email": "user@example.com",
  "reservation_number": "RES2024001",
  "event_name": "2024 서울 박람회"
}
```

### 3. 비밀번호 재설정 이메일 전송

**POST** `/senders/password/reset/`

요청 본문:
```json
{
  "target_email": "user@example.com",
  "reset_token": "abc123xyz",
  "limit_time": 24
}
```

### 4. 이메일 템플릿 조회

**GET** `/templates/`

모든 템플릿 목록을 반환합니다.

**GET** `/templates/{id}/`

특정 템플릿을 조회합니다.

### 5. 이메일 템플릿 수정

**PUT** `/templates/{id}/`

요청 본문:
```json
{
  "name": "비밀번호 재설정",
  "subject": "[MYCE] 비밀번호 재설정 안내",
  "content": "{\"emailTitle\": \"...\", \"preheader\": \"...\"}"
}
```

<br/>

## 데이터베이스 스키마

### MessageTemplate 테이블

```sql
CREATE TABLE MessageTemplate (
  id INT PRIMARY KEY AUTO_INCREMENT,
  code VARCHAR(20) NOT NULL,           # 템플릿 코드
  file_name VARCHAR(100) NOT NULL,     # HTML 파일명
  name VARCHAR(50) NOT NULL,           # 템플릿 이름
  subject VARCHAR(100) NOT NULL,       # 이메일 제목
  content LONGTEXT NOT NULL,           # JSON 형식의 템플릿 내용
  created_at DATETIME DEFAULT NOW(),
  updated_at DATETIME DEFAULT NOW()
);
```

### content 필드 구조 (JSON)

```json
{
  "preheader": "미리보기 텍스트",
  "emailTitle": "이메일 제목",
  "greetingMessage": "인사말",
  "verificationName": "인증 타입",
  "postMessage": "추가 메시지",
  "passwordLabel": "라벨",
  "warningPrefix": "경고 접두사",
  "warningMessage": "경고 메시지",
  "securityTitle": "보안 안내 제목",
  "securityContent": "보안 안내 내용"
}
```

<br/>

## 환경 변수

`.env` 파일에 다음 변수를 설정합니다:

```env
# 데이터베이스
DB_ENGINE={{ db_engine }}
DB_HOST={{ db_host }}
DB_PORT={{ db_port }}
DB_NAME={{ database_name }}
DB_USER={{ db_user }}
DB_PASSWORD={{ db_password }}

# 이메일 (AWS SES SMTP)
MAIL_FROM={{ default_from_email }} 
MAIL_REGION={{ aws_ses_region }}
MAIL_HOST={{ aws_ses_host }}
MAIL_USERNAME={{ aws-ses-username }}
MAIL_PASSWORD={{ aws-ses-password }}

SITE_URL={{ site_url }}
```

<br/>

## 주요 기능

### 1. 이메일 템플릿 관리

- 데이터베이스에서 이메일 템플릿을 관리합니다
- JSON 형식으로 유연한 콘텐츠 저장
- 관리자 페이지에서 쉽게 수정 가능

### 2. HTML 이메일 렌더링

Django의 `render_to_string()`을 사용하여 HTML 템플릿을 렌더링합니다:

```python
html_content = render_to_string(
    "mail-password.html",
    context
)
```

### 3. AWS SES SMTP 통합

`EmailMultiAlternatives`를 사용하여 HTML 이메일을 안전하게 전송:

```python
email = EmailMultiAlternatives(
    subject=subject,
    body='',
    from_email=from_email,
    to=[recipient_email]
)
email.attach_alternative(html_content, "text/html")
email.send()
```

### 5. 에러 처리 및 로깅

커스텀 예외를 사용하여 명확한 에러 처리:

```python
class EmailSendError(APIException):
    status_code = 500
    default_detail = '이메일 전송에 실패했습니다.'
    default_code = 'EMAIL_SEND_ERROR'
```

<br/>

## 개발 가이드

### 새로운 이메일 템플릿 추가

#### 1단계: 템플릿 코드 정의
`apps/templates/models.py`에 코드 추가:

```python
class MessageTemplateCode(models.TextChoices):
    NEW_EMAIL_TYPE = "NEW_EMAIL_TYPE"
```

#### 2단계: HTML 파일 생성
`resources/templates/`에 HTML 파일 생성:

```html
<!-- resources/templates/mail-new-type.html -->
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>{{ emailTitle }}</title>
</head>
<body>
  <h1>{{ emailTitle }}</h1>
  <p>{{ greetingMessage }}</p>
</body>
</html>
```

#### 3단계: 데이터베이스에 템플릿 저장
```python
MessageTemplate.objects.create(
    code='NEW_EMAIL_TYPE',
    file_name='mail-new-type',
    name='새 이메일 타입',
    subject='[MYCE] 새 이메일',
    content=json.dumps({
        "emailTitle": "...",
        "preheader": "...",
        # ...
    })
)
```

#### 4단계: 서비스 함수 작성
`apps/senders/services.py`에 함수 추가:

```python
def send_new_type_email(serializer_data: dict) -> bool:
    try:
        context = build_new_type_context(serializer_data)
        html_content = render_html(context['file_name'], context['context'])
        send(
            to=serializer_data['target_email'],
            subject=context['subject'],
            content=html_content
        )
        return True
    except EmailSendError as e:
        logger.error(f"Failed to send email: {str(e)}")
        raise
```

#### 5단계: API 엔드포인트 추가
`apps/senders/views.py`에 뷰 추가:

```python
class NewTypeMailSendView(GenericAPIView):
    serializer_class = NewTypeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        try:
            send_new_type_email(serializer.validated_data)
            return Response({'success': True}, status=200)
        except EmailSendError as e:
            return Response(
                {'success': False, 'message': str(e)},
                status=500
            )
```

#### 6단계: URL 라우팅 추가
`apps/senders/urls.py`에 URL 추가:

```python
urlpatterns = [
    path('new-type/', views.NewTypeMailSendView.as_view(), name='new-type-sender'),
]
```

<br/>

## 트러블슈팅

### SSL 인증서 오류

**오류**: `[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed`

**해결책**:
```bash
pip install certifi
```

