from django.urls import path
import apps.senders.views as views

urlpatterns = [
    path('verification/', views.VerificationMailSendView.as_view(), name='senders'),
]