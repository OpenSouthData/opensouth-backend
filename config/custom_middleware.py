import boto3
import os
from public.models import ClientIP
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework.exceptions import ValidationError
import json

class TranslationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 200 and response.data:
            target_language = self.get_target_language(request)
            response_data = self.translate_response(response.data, target_language)
            return JsonResponse(response_data, safe=False)

        return response

    def translate_response(self, response, target_language):
        translated_dict = self.translate_dict(response, target_language)
        return translated_dict

    def translate_dict(self, data, target_language):
        if isinstance(data, dict):
            translated_data = {}
            for key, value in data.items():
                if isinstance(value, str):
                    translated_text = self.translate_text(value, target_language)
                    translated_data[key] = translated_text
                elif isinstance(value, dict):
                    translated_data[key] = self.translate_dict(value, target_language)
                elif isinstance(value, list):
                    translated_data[key] = []
                    for item in value:
                        if isinstance(item, dict):
                            translated_data[key].append(self.translate_dict(item, target_language))

            return translated_data

    def get_target_language(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        try:
            client_ip = ClientIP.objects.filter(ip_address=ip).first()

            if client_ip:
                return client_ip.lang
            else:
                return "en"
            
        except ClientIP.DoesNotExist:

            return "en"

        

    def translate_text(text, target_language):

        session = boto3.Session(
        region_name=os.getenv("region"),
        aws_access_key_id=os.getenv("mail_access_id"),
        aws_secret_access_key=os.getenv("mail_secret_key")

        )
    
        translate_client = session.client('translate')
        if text:
    
            try:
                response = translate_client.translate_text(
                    Text=text,
                    SourceLanguageCode='en',
                    TargetLanguageCode=target_language
                )
                translated_text = response['TranslatedText']

                return translated_text
            
            except Exception as e:
                data = {
                    "error": "Error translating text",
                    "text": text,
                    "target_language": target_language,
                    "error_message": str(e)
                }
                raise ValidationError(data)
        else:
            return text


class SecuredHostMiddleware:

    def host(request):

        host = request.META.get('HTTP_HOST')

        if str(host) != os.getenv("api_host"):
            raise ValidationError("Invalid host")


