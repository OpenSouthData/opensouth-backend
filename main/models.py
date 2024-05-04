from typing import Any, Iterable
from django.db import models
from django.contrib.auth import get_user_model
import uuid 
from django.forms import model_to_dict
from django.core.exceptions import ValidationError
import hashlib
from django.utils.text import slugify
# Create your models here.



User = get_user_model()



class Categories(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=650)
    image = models.ImageField(upload_to="category_images/", null=True)
    slug = models.SlugField(max_length=650, null=True)
    views = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)
    description = models.TextField(null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        super(Categories, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.name}"
    
    def delete(self):
        self.is_deleted = True
        self.name = f"{self.name} -deleted-"
        self.slug = f"{self.slug} -deleted-"
        self.save()

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return None
    
    @property
    def data_count(self):
        from .models import Datasets
        return Datasets.objects.filter(category=self).count()
   

    






class Organisations(models.Model):

    """ users is the group of users that are in the organisation
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=650)
    slug = models.SlugField(max_length=650, null=True)
    description = models.TextField()
    logo = models.ImageField(upload_to="organisation_logo/", null=True)
    users = models.ManyToManyField(User, related_name="organisations_users", blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="organisation_user")
    dataset_count = models.IntegerField(default=0)
    status = models.CharField(max_length=250, default="pending", choices=(("pending", "pending"), ("approved", "approved"), ("rejected", "rejected")))
    type = models.CharField(max_length=250, default="null", choices=(("cooperate_organisation", "cooperate_organisation"), ("cooperate_society", "cooperate_society")))
    email = models.EmailField(null=True)
    linkedin = models.URLField(null=True)
    twitter = models.URLField(null=True)
    website = models.URLField(null=True)
    is_deleted = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):

        if self.is_deleted:

            self.slug = slugify(self.name) + "-deleted-"
            self.name = self.name + "-deleted-"

        else:
            self.slug = slugify(self.name)

        super(Organisations, self).save(*args, **kwargs)


    def __str__(self):
        return self.name
    
    def delete(self):
        self.is_deleted = True
        self.name = f"{self.name} -deleted-"
        self.slug = f"{self.slug} -deleted-"
        self.save()
    
    @property
    def users_data(self):
        list_data = []
        users = self.users.all()
        for user in users:
            data = model_to_dict(user, fields=["id", "first_name", "last_name", "email", "role", "image_url"])
            data["id"] = user.id
            data["image_url"] = user.image_url
            list_data.append(data)
        return list_data
    
    @property
    def logo_url(self):
        if self.logo:
            return self.logo.url
        return None
    
    @property
    def data_count(self):
        from .models import Datasets
        return Datasets.objects.filter(organisation=self, status='published').count()
    
    @property
    def downloads_count(self):

        from .models import DatasetFiles
        files = DatasetFiles.objects.filter(dataset__organisation=self, is_deleted=False)
        count = 0
        for file in files:
            count += file.download_count
        
        return count
    
    @property
    def views_count(self):

        from .models import Datasets
        views = Datasets.objects.filter(organisation=self, status='published', is_deleted=False)

        count = 0
        for view in views:
            count += view.views

        return count


       

    


class Datasets(models.Model):

    status_choices = (

        ("pending", "pending"),
        ("further_review", "further_review"),
        ("published", "published"),
        ("unpublished", "unpublished"),
        ("rejected", "rejected"),
    )



    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="dataset_user")
    title = models.CharField(max_length=650)
    slug = models.SlugField(max_length=650, null=True)
    type = models.CharField(max_length=200, null=True)
    license = models.CharField(max_length=650)
    description = models.TextField()
    dui = models.CharField(max_length=650, null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="category_datasets", null=True)
    update_frequency = models.CharField(max_length=650)
    image = models.ImageField(upload_to="dataset_images/", blank=True, null=True)
    organisation = models.ForeignKey(Organisations, on_delete=models.CASCADE, null=True, related_name="organisation_datasets")
    status = models.CharField(max_length=650, choices=status_choices, default="pending")
    tags = models.ManyToManyField("Tags", related_name="dataset_tags", blank=True)
    views = models.IntegerField(default=0)
    temporal_coverage = models.CharField(max_length=650)
    spatial_coverage = models.CharField(max_length=650, null=True)
    geojson = models.JSONField(null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):

        self.slug = slugify(self.title)
        if self.organisation:
            self.type = "organisation"
        else:
            self.type = "individual"

        super(Datasets, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.title} -status- {self.status}"
    
    def delete(self):
        self.is_deleted = True
        self.name = f"{self.title} -deleted-"
        self.slug = f"{self.slug} -deleted-"
        self.save()

    
    @property
    def tags_data(self):
        return [model_to_dict(tag, fields=["name"]) for tag in self.tags.all()]
    
    
    @property
    def publisher_data(self):
        if self.organisation:
            data = model_to_dict(self.organisation, fields=["id", "type", "name", "slug", "logo_url"])
            data["type"] = "organisation"
            data["logo_url"] = self.organisation.logo_url
            data["id"] = self.organisation.id
            data["slug"] = self.organisation.slug     

            return data
        
        else:
            data = model_to_dict(self.user, fields=["id", "type", "first_name", "last_name", "email", "role", "image_url"])
            data["image_url"] = self.user.image_url
            data["type"] = "individual"
            data["id"] = self.user.id

            return data
        
    @property
    def files_count(self):
        from .models import DatasetFiles
        return DatasetFiles.objects.filter(dataset=self).count()

    @property
    def files(self):
        from .models import DatasetFiles
        files = DatasetFiles.objects.filter(dataset=self, is_deleted=False)
        if files:
            list_data = []
            for file in files:
                data = model_to_dict(file, fields=["id", "file_name", "file_url", "format", "size", "sha256", "created_at", "updated_at"])
                data["id"] = file.id
                data["file_name"] = file.file_name if file.file_name else file.file_url.split("/")[-1].split(".")[0]
                data["file_url"] = file.file_url
                data["created_at"] = file.created_at
                data["updated_at"] = file.updated_at
                list_data.append(data)
            return list_data
        
        return []


class Tags(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=650)
    slug = models.SlugField(max_length=650, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tags, self).save(*args, **kwargs)
    

    def delete(self):
        self.is_deleted = True
        self.name = f"{self.name} -deleted-"
        self.slug = f"{self.slug} -deleted-"
        self.save()
        
    


class DatasetFiles(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dataset = models.ForeignKey(Datasets, on_delete=models.CASCADE, related_name="dataset_files", null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_dataset_files", null=True)
    file = models.FileField(upload_to="dataset_files/")
    file_name = models.CharField(max_length=100, null=True)
    format = models.CharField(max_length=100)
    sha256 = models.CharField(max_length=100, null=True)
    size = models.CharField(max_length=100)
    download_count = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.dataset.title} -- {self.format} -- {self.size}"
    
    def delete(self):
        self.is_deleted = True
        self.sha256 = f"{self.sha256} -deleted-"
        self.save()


    def save(self, *args, **kwargs):
        self.sha256 = hashlib.sha256(self.file.read()).hexdigest()
        super(DatasetFiles, self).save(*args, **kwargs)

    @property
    def file_url(self):
        return self.file.url
    
    @property
    def uploaded_by(self):
        return model_to_dict(self.user, fields=["id", "first_name", "last_name", "email", "role", "image_url"])
    
    @property
    def dataset_data(self):
        return model_to_dict(self.dataset, fields=["id", "title", "image_url", "organisation_data", "status"])
    






class VerificationPin(models.Model):


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pin = models.CharField(max_length=100)
    organisation = models.ForeignKey(Organisations, on_delete=models.CASCADE, related_name="organisation_verification_pin")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.organisation.name}"




class DatasetComments(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dataset = models.ForeignKey(Datasets, on_delete=models.CASCADE, related_name="dataset_comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_dataset_comments")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"comments -- {self.dataset.title} -- {self.user.email}"
    
    def delete(self):
        self.is_deleted = True
        self.save()
    
    @property
    def user_data(self):
        return model_to_dict(self.user, fields=["id", "first_name", "last_name", "email", "role", "image_url"])
    
    @property
    def dataset_data(self):
        return model_to_dict(self.dataset, fields=["id", "title", "image_url", "organisation_data", "status"])
    







class News(models.Model):


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=650)
    slug = models.SlugField(max_length=650, null=True)
    body = models.TextField()
    image = models.ImageField(upload_to="news_images/", null=True)
    status = models.CharField(max_length=250, default="draft", choices=(("draft", "draft"), ("published", "published"), ("unpublished", "unpublished")))
    views = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(News, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.title} -- {self.is_published}"



    def delete(self):
        self.is_deleted = True
        self.save()

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return None





class OrganisationRequests(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organisation = models.ForeignKey(Organisations, on_delete=models.CASCADE, related_name="organisation_requests")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_organisation_requests")
    status = models.CharField(max_length=250, default="pending", choices=(("pending", "pending"), ("approved", "approved"), ("rejected", "rejected")))
    is_accepted = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.organisation.name} -- {self.user.email}"
    
    def delete(self):
        self.is_deleted = True
        self.save()

    @property
    def user_data(self):
        data = model_to_dict(self.user, fields=["id", "first_name", "last_name", "email", "role", "image_url"])
        data["image_url"] = self.user.image_url
        return data

    @property
    def organisation_data(self):
        return model_to_dict(self.organisation, fields=["id", "name", "slug", "logo_url"])
    





class Support(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_support", null=True)
    name = models.CharField(max_length=650)
    email = models.EmailField(null=True)
    type = models.CharField(max_length=250, null=True)
    subject = models.CharField(max_length=650, null=True)
    message = models.TextField(null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return f"{self.name} -- {self.email}"
    


class CategoryAnalysis(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="category_analysis")
    attribute = models.CharField(max_length=650)
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.category.name} -- {self.attribute} -- {self.count}"
    



class LocationAnalysis(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dataset = models.ForeignKey(Datasets, on_delete=models.CASCADE, null=True, related_name="location_analysis")
    country = models.CharField(max_length=650)
    slug = models.SlugField(max_length=650, null=True)
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.country)
    #     super(LocationAnalysis, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.country} -- count- {self.count}"
    

