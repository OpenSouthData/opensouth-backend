from rest_framework import serializers
from .models import *








class TokenSerializer(serializers.ModelSerializer):


    class Meta:
        model = Token
        fields = '__all__'



        
class APIRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = APIRequest
        fields = '__all__'


class APIUsersSerializer(serializers.ModelSerializer):

    token_ = serializers.ReadOnlyField()
    user_ = serializers.ReadOnlyField()

    class Meta:
        model = APIUsers
        fields = '__all__'


