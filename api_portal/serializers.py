from rest_framework import serializers
from .models import *
from main.models import Datasets, DatasetFiles








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



class APIDatasetSerializer(serializers.ModelSerializer):
    category_ = serializers.ReadOnlyField()
    tags_data = serializers.ReadOnlyField()
    files_count = serializers.ReadOnlyField()
    publisher_ = serializers.ReadOnlyField()


    class Meta:
        model = Datasets
        fields = [ 'id', 'title', 'slug', 'license', 'description', 'dui', 'update_frequency', 'files_count', 'temporal_coverage', 'spatial_coverage', 'created_at', 'updated_at', 'geojson', 'tags_data', 'category_', 'publisher_' ]


class APIDatasetFilesSerializer(serializers.ModelSerializer):

    file_url = serializers.ReadOnlyField()

    class Meta:
        model = DatasetFiles

        fields = ['id', 'file_name', 'file_url', 'format', 'size', 'sha256', 'created_at', 'updated_at']
