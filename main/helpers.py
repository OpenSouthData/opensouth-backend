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

            # Generate a unique filename
            file_name = str(uuid.uuid4())[:12]  # 12 characters are enough
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = f"{file_name}.{file_extension}"

            # Upload the decoded data directly to S3
            try:
                settings.s3_client.put_object(
                    Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                    Key=f"dataset_files/{complete_file_name}",
                    Body=decoded_file,
                    ContentType='application/octet-stream'  # Set the appropriate MIME type if known
                )
            except NoCredentialsError:
                self.fail('s3_upload_failed')

            # Here we return the S3 URL or key as the field value
            return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/dataset_files/{complete_file_name}"

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
        

        





