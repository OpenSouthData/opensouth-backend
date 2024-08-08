import random 
from .models import VerificationPin
from rest_framework.exceptions import ValidationError




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



# serializers.py
import base64
import six
import uuid
from rest_framework import serializers
from config import settings
from botocore.exceptions import NoCredentialsError


class Base64FileField(serializers.FileField):
    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                # Extract the actual Base64 data from the input
                header, data = data.split(';base64,')
            try:
                # Decode the Base64 data
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_file')
            except Exception as e:
                raise ValidationError(f"error;  {e}")

            # Return the decoded file data for further processing
            return decoded_file

        self.fail('invalid_file')

            




class UploadBase64:

    def raw(self, data):

        base64 = data['file']
        name = data['file_name']
        file_format = data['format']

        # Decode the Base64 data
        decoded_file = base64.b64decode(base64)

        try:
            # Upload the decoded data directly to S3
            settings.s3_client.put_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=f"dataset_files/{name}",
                Body=decoded_file,
                ContentType=f"{file_format}" 
            )
        except Exception as e:
            raise ValidationError(f"error;  {e}")
        

        





