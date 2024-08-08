import requests
import os
from config.send_mail import send_email

from django.template.loader import render_to_string

key = os.getenv("email_key")








def organisation_actions_mail(user, message, action):

    
    body = f"""

        <p>Dear {str(user.first_name).capitalize()},</p>

        <p>{message}</p>

        <p>If you have any questions or need assistance, please contact our support team at support@opensouth.io.</p>
        <p>Best regards,</p>
        <p>Open South.</p>

    """
    html = render_to_string(
        'email/dataset.html',
        {
            'content': str(message),
            'name' : str(user.first_name).title()

        }
    )
    
    send_email(
        recipient=str(user.email),
        subject=f"Open South - Organisation {str(action).capitalize()}",
        body=body,
        html=html
    )






def dataset_actions_mail(user, message, action):

    body = f"""

        <p>Dear {str(user.first_name).capitalize()},</p>

        <p>{message}</p>

        <p>If you have any questions or need assistance, please contact our support team at support@opensouth.io.</p>
        <p>Best regards,</p>
        <p>Open South.</p>

    """
    html = render_to_string(
        'email/dataset.html',
        {
            'content': str(message),
            'name' : str(user.first_name).title()

        }
    )
    
    send_email(
        recipient=str(user.email),
        subject=f"Open South - Dataset {str(action).capitalize()}",
        body=body,
        html=html
    )

