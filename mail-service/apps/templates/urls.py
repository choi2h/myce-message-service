from django.urls import path
import apps.templates.views as views

urlpatterns = [
    path("", views.TemplateListView.as_view(), name="template-list"),
    path("<int:id>/", views.TemplateView.as_view(), name="template-detail"),
]