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


class PartnersSerializer(serializers.ModelSerializer):

    organisation_name = serializers.CharField(max_length=100, required=True)
    contact_person = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(max_length=15, required=True)
    organisation_type = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(max_length=100, required=True)

   
