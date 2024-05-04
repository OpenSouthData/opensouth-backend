from rest_framework import serializers
from .social_helpers import google
from .social_helpers.register import register_social_user
from rest_framework.exceptions import AuthenticationFailed
from config import settings






class GoogleSocialAuthSerializer(serializers.Serializer):

    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again.'
            )
        
        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            
            raise AuthenticationFailed('oops, who are you!?')

        # user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_user(
            provider=provider, email=email, name=name)


