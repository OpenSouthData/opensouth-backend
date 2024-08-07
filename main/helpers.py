import random 
from .models import VerificationPin





def generate_organisation_pin(organisation):

    """
    Generates a random 6 digit pin
    """
    
    pin = random.randint(100000, 999999)

    VerificationPin.objects.create(
        organisation=organisation,
        pin=pin
    )


    return pin





       

import base64
import imghdr
import uuid

from django.core.files.base import ContentFile
from rest_framework import serializers

class CustomBase64FileField(serializers.Field):
    def to_internal_value(self, data):
        # Check if this is a base64 string
        if isinstance(data, str):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            img_name = str(uuid.uuid4())[:12]  
            img_filename = f"{img_name}.{ext}"

            data = ContentFile(base64.b64decode(imgstr), name=img_filename)
        
        return super().to_internal_value(data)