from django.urls import path
from .views import (UserAccountDetailView, 
                    MobileAppForgotPasswordView, 
                    MobileAppEnterNewPasswordView, 
                    ResendRegistrationOTPCodeAPIView,
                    UserAccountUpdateDetailView, 
                    ProfileAccountUpdateDetailView,
                    CustomRegistrationAPIView,
                    CustomAccountActivationAPIView
                )

app_name = 'accounts_api'

urlpatterns = [
    path('register/', CustomRegistrationAPIView.as_view(), name='register'),
    path('activate-account/', CustomAccountActivationAPIView.as_view(), name='custom-activate-account'),
    path('resend-registration-otp-code/', ResendRegistrationOTPCodeAPIView.as_view(), name='resend-registration-otp-code'),
    path('account/<int:pk>/', UserAccountDetailView.as_view(), name='account-view'),
    path('account/update/<int:pk>/', UserAccountUpdateDetailView.as_view(), name='account-update-view'),
    path('profile/<int:pk>/', ProfileAccountUpdateDetailView.as_view(), name='profile-update-view'),

    path('forgot-password/', MobileAppForgotPasswordView.as_view(), name="forgot-password"),
    path('forgot-password/enter-new/', MobileAppEnterNewPasswordView.as_view(), name="forgot-password-enter-new"),
]