from rest_framework import serializers
from .models import ClientIP
from main.models import Tags, Support











class PublicTagSerializer(serializers.Serializer):

    class Meta:
        model = Tags
        fields = "__all__"




class ClientIPSerializer(serializers.ModelSerializer):

    class Meta:
        
        model = ClientIP
        fields = "__all__"

