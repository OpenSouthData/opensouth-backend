from django.db import models
import uuid

# Create your models here.









class ClientIP(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ip_address = models.CharField(max_length=650)
    lang = models.CharField(max_length=100)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "Client IP"
        verbose_name_plural = "Client IPs"

    def __str__(self):
        return f"{self.ip_address} -- {self.lang}"
    

    def delete(self):
        self.is_deleted = True
        self.save()
    