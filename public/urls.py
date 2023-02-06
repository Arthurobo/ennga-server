from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from .views import home

app_name = "account"

urlpatterns = [
     # Beginning Reset password
    path('', home, name='home'),
                                                                 
]
