from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
# from django.utils.translation import gettext_lazy as _
from public.models import ClientIP
from config.custom_middleware import TranslationMiddleware
from public.models import ClientIP
from .helpers import CustomBase64FileField
import uuid


User = get_user_model()






class OrganisationSerializer(serializers.ModelSerializer):


    logo = serializers.ImageField(required=False)
    data_count = serializers.ReadOnlyField()
    downloads_count = serializers.ReadOnlyField()
    views_count = serializers.ReadOnlyField()
    users_data = serializers.ReadOnlyField()
    logo_url = serializers.ReadOnlyField()
    email = serializers.EmailField(required=True)

    

    class Meta:
        model = Organisations
        fields = "__all__"

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

        if lang == "en":
            return representation

        representation['description'] = TranslationMiddleware.translate_text(text=representation['description'], target_language=lang)

        return representation


class DatasetSerializer(serializers.ModelSerializer):

    coordinates = serializers.CharField(read_only=True)

    
    publisher_data = serializers.ReadOnlyField()
    files = serializers.ReadOnlyField()
    tags_data = serializers.ReadOnlyField()
    views = serializers.ReadOnlyField()
    files_count = serializers.ReadOnlyField()

    class Meta:
        model = Datasets
        fields = "__all__"

    def to_representation(self, instance):

        request = self.context.get('request')
        id = request.GET.get('lang_id', None)
        if id:
            try:
                lang = ClientIP.objects.get(id=id).lang
            except ClientIP.DoesNotExist:
                raise serializers.ValidationError("clientIP instance not found")
       
            
            representation = super().to_representation(instance)

            if lang == "en":
                return representation

            representation['description'] = TranslationMiddleware.translate_text(text=representation['description'], target_language=lang)
            representation['title'] = TranslationMiddleware.translate_text(text=representation['title'], target_language=lang)
            representation['update_frequency'] = TranslationMiddleware.translate_text(text=representation['update_frequency'], target_language=lang)
            representation['license'] = TranslationMiddleware.translate_text(text=representation['license'], target_language=lang)

            return representation
        
        else:
            return super().to_representation(instance)



class DatasetFileSerializer(serializers.ModelSerializer):

    dataset_data = serializers.ReadOnlyField()
    file_url = serializers.ReadOnlyField()
    file = CustomBase64FileField(required=True)
    # file = serializers.FileField(required=True)
    uploaded_by = serializers.ReadOnlyField()

    class Meta:
        model = DatasetFiles
        fields = "__all__"




class CategorySerializer(serializers.ModelSerializer):

    data_count = serializers.ReadOnlyField()
    image_url = serializers.ReadOnlyField()

    class Meta:
        model = Categories
        fields = "__all__"
    

    def to_representation(self, instance):

        request = self.context.get('request')
        id = request.GET.get('lang_id', None)
        if id:
            try:
                lang = ClientIP.objects.get(id=id).lang
            except ClientIP.DoesNotExist:
                raise serializers.ValidationError("clientIP instance not found")
        
            
            representation = super().to_representation(instance)

            if lang == "en":
                return representation

            representation['description'] = TranslationMiddleware.translate_text(text=representation['description'], target_language=lang)
            representation['name'] = TranslationMiddleware.translate_text(text=representation['name'], target_language=lang)

            return representation
        else:
            return super().to_representation(instance)



class TagsSerializer(serializers.ModelSerializer):

    keywords = serializers.ListField(child=serializers.CharField(max_length=5000), write_only=True, required=True)
    name = serializers.CharField(max_length=100, required=False)


    extra_kwargs = {
            'keywords': {'write_only': True},
        }


    class Meta:
        model = Tags
        fields = ["id", "name", "slug", "is_deleted", "created_at", "updated_at", "keywords"]







class PinSerializer(serializers.Serializer):

    pin = serializers.CharField(max_length=6, required=True)



class DatasetCommentSerializer(serializers.ModelSerializer):

    dataset_data = serializers.ReadOnlyField()
    user_data = serializers.ReadOnlyField()
    
    class Meta:
        model = DatasetComments
        fields = "__all__"




class NewsSerializer(serializers.ModelSerializer):

    image_url = serializers.ReadOnlyField()
    class Meta:
        model = News
        fields = "__all__"

    def to_representation(self, instance):

        request = self.context.get('request')
        id = request.GET.get('lang_id', None)
        if id:
            try:
                lang = ClientIP.objects.get(id=id).lang
            except ClientIP.DoesNotExist:
                raise serializers.ValidationError("clientIP instance not found")

            
            representation = super().to_representation(instance)

            if lang == "en":
                return representation

            representation['body'] = TranslationMiddleware.translate_text(text=representation['body'], target_language=lang)

            return representation
        
        else:
            return super().to_representation(instance)




class OrganisationRequestSerializer(serializers.ModelSerializer):

    organisation_data = serializers.ReadOnlyField()
    user_data = serializers.ReadOnlyField()

    class Meta:
        model = OrganisationRequests
        fields = "__all__"



class SupportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Support
        fields = "__all__"



class LocationAnalysisSerializer(serializers.ModelSerializer):

    class Meta:
        model = LocationAnalysis
        fields = "__all__"



