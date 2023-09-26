import random

from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics


from accounts.models import Account, Profile, MobileAppAccountAuthenticationRequest
from accounts.tasks import send_password_activate_token_to_user, send_password_reset_token_to_user, send_password_change_token_to_user
from .serializers import (CustomRegistrationSerializer, 
                            MobileAppAccountAuthenticationRequestSerializer, 
                            AccountSerializer, 
                            ForgotPasswordSerializer,
                            MobileAppEnterNewPasswordSerializer, 
                            ResendRegistrationOTPCodeSerializer, 
                            AccountUpdateSerializer,
                            ProfileDetailSerializer,
                            ProfileUpdateSerializer
                        )


class CustomRegistrationAPIView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = CustomRegistrationSerializer
    permission_classes = (permissions.AllowAny,)


class ResendRegistrationOTPCodeAPIView(generics.CreateAPIView):
    queryset = MobileAppAccountAuthenticationRequest.objects.all()
    serializer_class = ResendRegistrationOTPCodeSerializer

    def perform_create(self, serializer):
        user_email = self.request.data.get("email", None)
        _activate_account_code = random.randint(100000, 999999)
        user_account = Account.objects.filter(email=user_email)[0]
        user_account_update = Account.objects.filter(email=user_email).update(activate_account_code=_activate_account_code)

        user_account_id = user_account.id
        print(user_account_id)
        print(type(user_account_id))
        new_account_id = user_account.id
        email = send_password_activate_token_to_user(new_account_id)
        return user_account


class CustomAccountActivationAPIView(generics.CreateAPIView):
    queryset = MobileAppAccountAuthenticationRequest.objects.all()
    serializer_class = MobileAppAccountAuthenticationRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(**{'data': request.data})
        serializer.is_valid()
        data = request.data
        entered_activate_account_code = serializer.data['activate_account_code']

        if Account.objects.filter(activate_account_code=entered_activate_account_code).exists():
            user = Account.objects.get(activate_account_code=entered_activate_account_code)
            Account.objects.filter(activate_account_code=entered_activate_account_code).update(is_active=True)

            # Empty code string
            empty_code_string = ''
            Account.objects.filter(activate_account_code=entered_activate_account_code).update(activate_account_code=empty_code_string)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # raise Http404
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
            # return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)


class UserAccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_update(self, serializer):
        instance = serializer.save()
        # send_email_confirmation(user=self.request.user, modified=instance)


class UserAccountUpdateDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Account.objects.all()
    serializer_class = AccountUpdateSerializer
    # parser_classes = [MultiPartParser, FormParser]

    # def perform_update(self, serializer):
    #     instance = serializer.save()
    #     # send_email_confirmation(user=self.request.user, modified=instance)


class ProfileAccountUpdateDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    # parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ProfileUpdateSerializer
        else:
            return ProfileDetailSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        # send_email_confirmation(user=self.request.user, modified=instance)


class MobileAppForgotPasswordView(generics.CreateAPIView):
    queryset = MobileAppAccountAuthenticationRequest.objects.all()
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(**{'data': request.data})
        serializer.is_valid()
        # serializer.save()
        # if 
        entered_email = serializer.data['email']
        accounts = Account.objects.all()

        if Account.objects.filter(email=entered_email).exists():
            # print("Account Rhyme oh")
            user_account_id = Account.objects.get(email=entered_email)
            account_id = user_account_id.id
            _forgot_password_code = random.randint(100000, 999999)
            Account.objects.filter(email=entered_email).update(forgot_password_code=_forgot_password_code)
            # print(_forgot_password_code)

            # Send password reset token to user
            send_password_reset_token_to_user(account_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            # print("Account no Rhyme oh")
            # pass

            # return Response(status=status.HTTP_201_CREATED)
            # raise Http404
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)


class MobileAppEnterNewPasswordView(generics.CreateAPIView):
    queryset = MobileAppAccountAuthenticationRequest.objects.all()
    serializer_class = MobileAppEnterNewPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(**{'data': request.data})
        serializer.is_valid()
        
        data = request.data
        entered_forgot_password_code = serializer.data['forgot_password_code']
        entered_password = serializer.data['password']

        try:
            user = Account.objects.get(forgot_password_code=entered_forgot_password_code)
        except:
            error_message = "Invalid or expired token"
            return Response(data={"error": error_message}, status=status.HTTP_401_UNAUTHORIZED)


        if Account.objects.filter(forgot_password_code=entered_forgot_password_code).exists():
            if user:
                user.set_password(entered_password)
                user.save()
                # I am not returning serializer.data below cos of security reasons
                return Response(status=status.HTTP_201_CREATED)
            else:
                # raise Http404
                # I am not returning serializer.data below cos of security reasons
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            # raise Http404
            # I am not returning serializer.data below cos of security reasons
            return Response(status=status.HTTP_404_NOT_FOUND)


# This is when a user wants to reset their password when they are already logged in
class MobileAppChangePasswordView(generics.CreateAPIView):
    queryset = MobileAppAccountAuthenticationRequest.objects.all()
    serializer_class = ForgotPasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(**{'data': request.data})
        serializer.is_valid()
        # serializer.save()
        # if 
        entered_email = serializer.data['email']
        accounts = Account.objects.all()

        if Account.objects.filter(email=entered_email).exists():
            # print("Account Rhyme oh")
            user_account_id = Account.objects.get(email=entered_email)
            account_id = user_account_id.id
            _forgot_password_code = random.randint(100000, 999999)
            Account.objects.filter(email=entered_email).update(forgot_password_code=_forgot_password_code)
            # print(_forgot_password_code)

            # Send password reset token to user
            send_password_change_token_to_user(account_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            # print("Account no Rhyme oh")
            # pass

            # return Response(status=status.HTTP_201_CREATED)
            # raise Http404
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)


# # START HERE
# 1. Profile Detail - Profile models (You can easily call both the Profile and the Account objects in a single API endpoint)
# 2. Profile Update - Profile models
# 3. Account Update - Account models