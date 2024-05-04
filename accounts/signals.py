import random
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from config import settings
from djoser.signals import user_registered, user_activated
from .emails import *

from .models import ActivationOtp
from django.utils import timezone
from django.core.mail import send_mail
from config.send_mail import send_email
from django.template.loader import render_to_string
import json
import os
import  requests


User = get_user_model()
site_name = ""


def generate_otp(n):
    return "".join([str(random.choice(range(10))) for _ in range(n)])


            
@receiver(user_registered)
def activate_otp(user, request, *args,**kwargs):
    
    if user.role == "user":
        user.is_active = False
        user.save()
        
        code = generate_otp(6)
        expiry_date = timezone.now() + timezone.timedelta(minutes=10)
        ActivationOtp.objects.create(code=code, expiry_date=expiry_date, user=user)
        subject = "Open South - Account Activation"
        
        message = f"""Hi, {str(user.first_name).title()}.

To authenticate, please use the following One Time Password (OTP):

{code}

Please do not share this OTP with anyone. At Open South, we take your account security very seriously. 
Our Support Team will never ask you to disclose or verify your password, OTP and other personal information.
If you did not initiate this request, please contact our support team immediately.


"""   
       
        
        recipient_list = [user.email]
        html = render_to_string('email/activation.html', {'name': str(user.first_name).title(), 'code':code})
        send_email(
            subject=subject,
            body=message,
            recipient=recipient_list[0],
            html=html
        )
        
        
        return






@receiver(user_activated)
def comfirmaion_email(user, request, *args,**kwargs):
    
    if user.role == "user":
        if user.is_active:
            subject = "Welcome to Open South"
        
            message = f"""

Dear {str(user.first_name).title()},

Welcome to the Open South open data platform

We are thrilled to welcome you to our community and excited to embark on the journey of exploring and utilizing open data in innovative ways.

As a member of Open South, you will have access to a wealth of data resources, tools, and collaboration opportunities. Whether you are a data enthusiast, researcher, or an organization passionate about data-driven solutions, our platform is designed to cater to your needs.

Your benefits as a member:

Access to high-quality data: Our platform hosts a diverse range of high-quality datasets from various domains. Explore, analyze, and utilize these datasets to drive your projects and initiatives.

Community collaboration: Connect with like-minded data curators, researchers, and organizations. Share your insights, collaborate on projects, and learn from a vibrant and diverse community.

Innovative tools and resources: We provide tools and resources to help you work with data effectively. Whether you are a beginner or an expert, our resources are here to support your journey.

News and updates: Stay informed about the latest developments, events, and opportunities related to open data and data-driven projects.

To get started, log in to your account using the credentials you provided during registration. If you have any questions or need assistance, reach out to our support team at support@opensouth.io.

Thank you for choosing Open South. We are excited to see the incredible contributions you will make to our data community.

Best regards,

Open South.

"""   
       
        
        recipient_list = [user.email]
        html = render_to_string('email/confirmation.html', {'name': str(user.first_name).title()})
        send_email(
            subject=subject,
            body=message,
            recipient=recipient_list[0],
            html=html
        )
        
        
        return
    