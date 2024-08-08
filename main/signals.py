import random
from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from config import settings
from djoser.signals import user_registered, user_activated
from .email import *
from .helpers import *

from django.utils import timezone
from .models import *





@receiver(post_save, sender=Organisations)
def organisation_created_mail(sender, instance, created, **kwargs):

    if created:
        
        pin = generate_organisation_pin(organisation=instance)

        organisation_verification_email(email=instance.email, user=instance.user, organization=instance, pin=pin)


        return


@receiver(post_save, sender=Datasets)
def dataset_created(sender, instance, created, **kwargs):

    if created:

        if instance.organisation:

            message = f"""
A new dataset with the DUI id: {str(instance.dui)} has been created under the {str(instance.organisation.name).capitalize()} organisation. 
Please visit the following link to view the dataset:
<a
    href=https://opensouth.io/dataset/{instance.pk}
    >
    https://opensouth.io/dataset/{instance.pk}
</a>.

"""
            users = instance.organisation.users.all()

            for user in users:
                email = user.email

                dataset_created_mail(email=email, user=user, message=message)

            return


        else:
                
            user = instance.user
            email = instance.user.email
            message = f"""
A new dataset with the DUI id: {instance.dui} has been created under your account.
Please visit the following link to view the dataset: https://opensouth.io/dataset/{instance.pk}.

"""
            dataset_created_mail(email=email, user=user, message=message)



            return
        
      

to = 'support@opensouth.io'


@receiver(post_save, sender=Support)
def support_mail(sender, instance, created, **kwargs):

    if created:
        if instance.type == 'public':
            public_support_mail(to=to, name=instance.name, message=instance.message, address=instance.email)

            return 
        return
    return


        
       