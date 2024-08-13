from django.urls import path
from .views import ContactUsAPIView

app_name = 'public_api'
urlpatterns = [
    path("contact-us/",ContactUsAPIView.as_view(), name="contact-us")
]


