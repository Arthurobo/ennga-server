from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from .views import dashboard, edit_account_view, UpdatePassword

app_name = "platform_admin"

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('<user_id>/edit/', edit_account_view, name='edit-account'),
    path('change-password/', UpdatePassword.as_view(), name="update_password"),
                                                                 
]
