from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.signals import user_activated
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from config.translate import TranslationMiddleware
from .emails import *
from public.models import ClientIP
from .models import ActivationOtp
from .signals import generate_otp, site_name
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import Permission, Group
from drf_extra_fields.fields import Base64ImageField
import uuid
from config import settings
 
User = get_user_model()

        

class UserRegistrationSerializer(BaseUserRegistrationSerializer):
    
    class Meta(BaseUserRegistrationSerializer.Meta):
        fields = ['id', "first_name", "last_name", "email", "role", "password", "is_active"]
        
    
class UserDeleteSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"})

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type": "password"}, write_only=True, required=False)
    image_url = serializers.ReadOnlyField()
    organisations = serializers.ReadOnlyField()
    
    class Meta():
        model = User
        fields = ['id', "first_name", "last_name", "email", "password", "bio", "is_active", "role", "groups", "user_permissions", "is_superuser", "image_url", "date_joined", "organisations", "user_stats", "meta"]

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def to_representation(self, instance):
        
        request = self.context.get('request')
        id = request.GET.get('lang_id', None)
        if id:
            try:
                lang = ClientIP.objects.get(id=id).lang
            except ClientIP.DoesNotExist:
                raise serializers.ValidationError("clientIP instance not found")
        else:
            lang = "en"
            
        representation = super().to_representation(instance)

        representation['bio'] = TranslationMiddleware.translate_text(text=representation['bio'], target_language=lang)

        return representation
        


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=300)
    
    
class FirebaseSerializer(serializers.Serializer):
    fcm_token = serializers.CharField(max_length=5000)


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=700) 
    

class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    
    
    def verify_otp(self, request):
        otp = self.validated_data['otp']
        
        if ActivationOtp.objects.filter(code=otp).exists():
            try:
                otp = ActivationOtp.objects.get(code=otp)
            except Exception:
                ActivationOtp.objects.filter(code=otp).delete()
                raise serializers.ValidationError(detail='Cannot verify otp. Please try later')
            
            if otp.is_valid():
                if otp.user.is_active == False:
                    otp.user.is_active=True
                    otp.user.save()
                    
                    #clear all otp for this user after verification
                    all_otps = ActivationOtp.objects.filter(user=otp.user)
                    all_otps.delete()
                    user_activated.send(User, user=otp.user, request=request)
                    return {'message': 'Verification Complete'}
                else:
                    raise serializers.ValidationError(detail='User with this otp has been verified before.')
            
                
            else:
                raise serializers.ValidationError(detail='OTP expired')
                    
        
        else:
            raise serializers.ValidationError(detail='Invalid OTP')
    

class NewOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
     
    def get_new_otp(self):
        try:
            user = User.objects.get(email=self.validated_data['email'], is_active=False)
        except User.DoesNotExist:
            raise serializers.ValidationError(detail='Please confirm that the email is correct and has not been verified')
        
        code = generate_otp(6)
        expiry_date = timezone.now() + timezone.timedelta(minutes=10)
        
        ActivationOtp.objects.create(code=code, user=user, expiry_date=expiry_date)
        requestotp_mail(email=user.email, otp=code, name=str(user.first_name.title()))
        
        return {'message': 'Please check your email for OTP.'}
    

   
class PasswordOTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    password = serializers.CharField()
    re_password = serializers.CharField()
    
    def verify_otp(self, request, data):
        otp = self.validated_data['otp']
        
        if ActivationOtp.objects.filter(code=otp).exists():
            try:
                otp = ActivationOtp.objects.get(code=otp)
            except Exception:
                ActivationOtp.objects.filter(code=otp).delete()
                raise serializers.ValidationError(detail='Cannot verify otp. Please try later')
            
            if otp.is_valid():
                    otp.user.set_password(data['password'])
                    otp.user.save()
                    
                
                    all_otps = ActivationOtp.objects.filter(user=otp.user)
                    all_otps.delete()
                    
                    return {'message': 'Password reset Complete'}
            
                
            else:
                raise serializers.ValidationError(detail='OTP expired')
                    
        
        else:
            raise serializers.ValidationError(detail='Invalid OTP')
        
        
    def validate(self, attrs):
        if attrs['password'] != attrs["re_password"]:
            raise ValidationError(detail={"error":"passwords don't match"})
        return super().validate(attrs)

    
    
class PermissionSerializer(serializers.ModelSerializer):
    
    class Meta:
        fields = "__all__"
        model = Permission

    
class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()


class EmailSerializer(serializers.Serializer):
    
    email = serializers.EmailField(required=True)




class PasswordResetSerializer(serializers.Serializer):

    password = serializers.CharField(required=True)
    re_password = serializers.CharField(required=True)


    def validate(self, attrs):
        if attrs['password'] != attrs["re_password"]:
            raise ValidationError(detail={"error":"passwords don't match"})
        return super().validate(attrs)



    