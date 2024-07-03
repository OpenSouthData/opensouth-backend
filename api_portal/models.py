from typing import Any
from django.db import models
import uuid
from django.contrib.auth import get_user_model
from datetime import datetime
from django.forms import model_to_dict


# Create your models here.



User = get_user_model()







class Token(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_token")
    token = models.CharField(max_length=6500)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.user.email
    
    def save(self, *args, **kwargs):

        if not self.token:
            self.token = self.generate_tokem()
        super(Token, self).save(*args, **kwargs)

    

    def delete_token(self):

        self.is_deleted = True
        self.is_active = False
        self.token = f"{self.token}--deleted--{datetime.now().date()}"
        self.save()

    def generate_tokem(self):
        
        parts = str(uuid.uuid4()).split('-')

        return ''.join(parts).lower()
    



class APIRequest(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    token = models.ForeignKey(Token, on_delete=models.CASCADE, related_name="token_api_request")
    meta = models.JSONField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.user.email
    
    # def save(self, *args, **kwargs):
    #     super(APIRequest, self).save(*args, **kwargs)


    def delete_request(self):

        self.is_deleted = True
        self.save()



class APIUsers(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_api_users")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)



    def __str__(self):
        return self.user.email
    
    def de_activate(self):
        self.is_active = False
        self.save()

    def re_activate(self):
        self.is_active = True
        self.save()

    def delete_user(self):
        self.is_deleted = True
        self.save()
    

    @property
    def token_(self):
        token = Token.objects.filter(user=self.user, is_active=True).first()
        if token:
            return model_to_dict(token)
        return None

        


