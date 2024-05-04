from rest_framework import serializers
from .models import TokenManager








class TokenSerializer(serializers.ModelSerializer):


    class Meta:
        model = TokenManager
        fields = '__all__'



        