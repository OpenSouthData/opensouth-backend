from accounts.permissions import *
from .serializers import *
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model
from .helpers.generators import generate_password
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed, NotFound, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate, logout
from django.contrib.auth.signals import user_logged_in, user_logged_out
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView , RetrieveUpdateAPIView
from rest_framework.decorators import action
from main.models import *
from main.serializers import *
from .emails import login_mail
from djoser.views import UserViewSet
from rest_framework.views import APIView
from .models import ActivityLog
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import Permission, Group
from django.db.models import Q
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.response import Response
import requests
import os



 
 
User = get_user_model()


def get_query():
    
    """returns query to be used to in the permissions view"""
    
    exclude_words = [ "activationotp", "activitylog", "moduleaccess", "logentry","group", "permission", "contenttype", "userinbox", "validationotp", "session", "blacklistedtoken", "outstandingtoken", "cart", ]
    
    query = Q()
    for word in exclude_words:
        query |= Q(codename__icontains=word)
        
    return query
    
   



class CustomUserViewSet(UserViewSet):
    queryset = User.objects.filter(is_deleted=False)
    
    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(role="user")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_Response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get("current_password")
        
        if check_password(password, instance.password):
            
            self.perform_destroy(instance)
            ActivityLog.objects.create(
                user=instance,
                action = f"Deleted account"
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        elif request.user.role == "admin" and check_password(password, request.user.password):
            self.perform_destroy(instance)
            ActivityLog.objects.create(
                user=request.user,
                action = f"Deleted account with ID {instance.id}"
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        
        else:
            raise AuthenticationFailed(detail={"message":"incorrect password"})


class AdminListCreateView(ListCreateAPIView):
    
    
    queryset = User.objects.filter(is_deleted=False, is_active=True, role="admin").order_by('-date_joined')
    serializer_class =  CustomUserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomDjangoModelPermissions]
    
    
    @swagger_auto_schema(method="post", request_body= CustomUserSerializer())
    @action(methods=["post"], detail=True)
    def post(self, request, *args, **kwargs):
        
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            
            if serializer.validated_data.get('is_superuser') == True and request.user.is_superuser == True:
                
                serializer.validated_data['is_superuser'] == True
                serializer.validated_data['is_staff'] == True
                
                
            elif serializer.validated_data.get('is_superuser', None) != True  :
                serializer.validated_data['is_superuser'] == False
                serializer.validated_data['is_staff'] == False
            
            else:
                raise PermissionDenied(detail={"message": "you do not have permission to perform this action"})
            
            serializer.validated_data['password'] = generate_password()
            serializer.validated_data['is_active'] = True
            serializer.validated_data['is_admin'] = True
            serializer.validated_data['role'] = "admin"
            instance = serializer.save()
            
            data = {
                'message' : "success",
                'data' : serializer.data,
            }
            
            ActivityLog.objects.create(
            user=request.user,
            action = f"Created admin with email {instance.email}"
            )

            return Response(data, status = status.HTTP_201_CREATED)

        else:
            data = {

                'message' : "failed",
                'error' : serializer.errors,
            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)
            



@swagger_auto_schema(methods=['POST'], request_body=PasswordOTPVerifySerializer())
@api_view(['POST'])
def reset_password_otp_verification(request):
    
    """Api view for verifying OTPs for password reset """

    if request.method == 'POST':

        serializer = PasswordOTPVerifySerializer(data = request.data)

        if serializer.is_valid():
            data = serializer.verify_otp(request, data=serializer.validated_data)
            
            return Response(data, status=status.HTTP_200_OK)
        else:

            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
            



@swagger_auto_schema(method='post', request_body=LoginSerializer())
@api_view([ 'POST'])
def user_login(request):
    
    """Allows users to log in to the platform. Sends the jwt refresh and access tokens."""
    
    if request.method == "POST":
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = authenticate(request, email = data['email'], password = data['password'], is_deleted=False)

            if user:
                if user.is_active==True:
                
                    try:
                        
                        refresh = RefreshToken.for_user(user)

                        user_detail = {}
                        user_detail['id']   = user.id
                        user_detail['first_name'] = user.first_name
                        user_detail['last_name'] = user.last_name
                        user_detail['email'] = user.email
                        user_detail['role'] = user.role
                        user_detail['is_admin'] = user.is_admin
                        user_detail['is_superuser'] = user.is_superuser
                        user_detail['access'] = str(refresh.access_token)
                        user_detail['refresh'] = str(refresh)
                        user_logged_in.send(sender=user.__class__,
                                            request=request, user=user)
                            
                        data = {
    
                        "message":"success",
                        'data' : user_detail,
                        }

                        login_mail(email=user.email, name=user.first_name)
             
                        return Response(data, status=status.HTTP_200_OK)
                    

                    except Exception as e:
                        raise e
                
                else:
                    data = {
                    
                    'error': 'This account has not been activated'
                    }
                return Response(data, status=status.HTTP_403_FORBIDDEN)

            else:
                data = {
                    
                    'error': 'Please provide a valid email and a password'
                    }
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
                data = {
                    
                    'error': serializer.errors
                    }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            
            
@swagger_auto_schema(method="post",request_body=LogoutSerializer())
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Log out a user by blacklisting their refresh token then making use of django's internal logout function to flush out their session and completely log them out.

    Returns:
        Json Response with message of success and status code of 204.
    """
    
    serializer = LogoutSerializer(data=request.data)
    
    serializer.is_valid(raise_exception=True)
    
    try:
        token = RefreshToken(token=serializer.validated_data["refresh_token"])
        token.blacklist()
        user=request.user
        user_logged_out.send(sender=user.__class__,
                                        request=request, user=user)
        logout(request)
        
        return Response({"message": "success"}, status=status.HTTP_204_NO_CONTENT)
    except TokenError:
        return Response({"message": "failed", "error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)





@swagger_auto_schema(method="patch",request_body=FirebaseSerializer())
@api_view(["PATCH"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_firebase_token(request):
    """Update the FCM token for a logged in use to enable push notifications

    Returns:
        Json Response with message of success and status code of 200.
    """
    
    serializer = FirebaseSerializer(data=request.data)
    
    serializer.is_valid(raise_exception=True)
    
    fcm_token = serializer.validated_data.get("fcm_token")

    request.user.fcm_token = fcm_token
    request.user.save()
        
    return Response({"message": "success"}, status=status.HTTP_200_OK)
    



@swagger_auto_schema(methods=['POST'],  request_body=NewOtpSerializer())
@api_view(['POST'])
def reset_otp(request):
    if request.method == 'POST':
        serializer = NewOtpSerializer(data = request.data)
        if serializer.is_valid():
            data = serializer.get_new_otp()
            
            return Response(data, status=status.HTTP_200_OK)
        
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        
            
@swagger_auto_schema(methods=['POST'], request_body=OTPVerifySerializer())
@api_view(['POST'])
def otp_verification(request):
    
    """Api view for verifying OTPs """

    if request.method == 'POST':

        serializer = OTPVerifySerializer(data = request.data)

        if serializer.is_valid():
            data = serializer.verify_otp(request)
            
            return Response(data, status=status.HTTP_200_OK)
        else:

            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


class PermissionList(ListAPIView):
    serializer_class = PermissionSerializer
    queryset = Permission.objects.exclude(get_query())
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
  
        
        
@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def activity_logs(request):
    
    """shows 10 most recent logged user activities"""
    
    logs = ActivityLog.objects.filter(is_deleted=False, user=request.user).order_by("-date_created").values("action")[:10]
    
    return Response(logs, status=status.HTTP_200_OK)



@swagger_auto_schema(method="post", request_body=ImageUploadSerializer())
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def image_upload(request):
    
    if request.method == "POST":
        serializer = ImageUploadSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.image = serializer.validated_data.get("image")
        user.save()
        
        return Response({"message": "upload successful"}, status=status.HTTP_200_OK)






class PasswordResetView(APIView):
    serializer_class = EmailSerializer


    @swagger_auto_schema(method="post", request_body=EmailSerializer())
    @action(methods=["post"], detail=True)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user = User.objects.filter(email=email, is_deleted=False).first()
        
        if user:
            if user.is_active:

                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(user)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                referer = request.META.get('HTTP_REFERER')
                reset_url = f"{referer}reset-password/{uidb64}/{token}"
                reset_password_mail(email=email, url=reset_url, name=user.first_name.title())

                return Response({"message": "Reset password mail sent"}, status=200)
            
            else:
                return Response({"error": "account not activated"}, status=403)
        
        else:
            return Response({"error": "user not found"}, status=404)
        



class PasswordResetConfirmView(APIView):

    @swagger_auto_schema(method="post", request_body=PasswordResetSerializer())
    @action(methods=["post"], detail=True)
    def post(self, request, uidb64, token):

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        
        if user is not None and PasswordResetTokenGenerator().check_token(user, token):
            serializer = PasswordResetSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user.set_password(serializer.data.get("password"))
            user.save()

            return Response({"message": "password reset successful"}, status=200)
        
        else:
            return Response({"error": "invalid token"}, status=400)
        






        
@swagger_auto_schema(methods=['POST'], request_body=PinSerializer())
@api_view(['POST'])
def pin_verification(request):

    if request.method == 'POST':
        
        serializer = PinSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        pin = serializer.validated_data['pin']

        if VerificationPin.objects.filter(pin=pin).exists():

            verify_pin = VerificationPin.objects.get(pin=pin)

            if verify_pin.is_active == False:
                return Response({"error": "pin has been used"}, status=400)
            
            if verify_pin.organisation.is_verified:
                return Response({"error": "organisation already verified"}, status=400)
            
            verify_pin.is_active = False
            verify_pin.save()

            verify_pin.organisation.is_verified = True
            verify_pin.organisation.save()

            return Response({"message": "organisation verified successfully"}, status=200)
        
        return Response({"error": "invalid pin"}, status=400)

