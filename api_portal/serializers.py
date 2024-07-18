from rest_framework import serializers
from .models import *
from main.models import Datasets








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


    class Meta:
        model = Datasets
        fields = [ 'id', 'title', 'slug', 'license', 'description', 'dui', 'category', 'update_frequency', 'image', 'status', 'temporal_coverage', 'spatial_coverage', 'created_at', 'updated_at', 'geojson', 'tags_data', 'category_' ]




    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # user = modeals.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="dataset_user")
    # title = models.CharField(max_length=650)
    # slug = models.SlugField(max_length=650, null=True)
    # type = models.CharField(max_length=200, null=True)
    # license = models.CharField(max_length=650)
    # description = models.TextField()
    # dui = models.CharField(max_length=650, null=True)
    # category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="category_datasets", null=True)
    # update_frequency = models.CharField(max_length=650)
    # image = models.ImageField(upload_to="dataset_images/", blank=True, null=True)
    # organisation = models.ForeignKey(Organisations, on_delete=models.CASCADE, null=True, related_name="organisation_datasets")
    # status = models.CharField(max_length=650, choices=status_choices, default="pending")
    # tags = models.ManyToManyField("Tags", related_name="dataset_tags", blank=True)
    # views = models.IntegerField(default=0)
    # temporal_coverage = models.CharField(max_length=650)
    # spatial_coverage = models.CharField(max_length=650, null=True)
    # geojson = models.JSONField(null=True)
    # is_deleted = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)