import requests
import os
from config.send_mail import send_email
from django.template.loader import render_to_string






   
def organisation_add_users(user, organisation):

    message = f"""

Dear {str(user.first_name).title()},

You have been invited  into the organisation {str(organisation.name).capitalize()} to become a colaborator.

If you encounter any issues during the process or have any questions about our platform,
please don't hesitate to reach out to our friendly support team at support@opensouth.io

Best regards,
Open South.

"""
    html = render_to_string(
        'email/dataset.html',
        {
            'content': f"You have been invited  into the organisation {str(organisation.name).capitalize()} to become a colaborator.",
            'name' : str(user.first_name).title()

        }
    )
    send_email(
        recipient=user.email,
        subject="Open South - Organisation Invitation",
        body=message,
        html=html
    )

   
def organisation_delete_users(user, organisation):

    message = f"""

Dear {str(user.first_name).capitalize()},

You have been removed from the organisation {str(organisation.name).capitalize()}.
If you think this was an error or unintended, feel free to reach out to our support team.

If you encounter any issues during the process or have any questions about our platform,
please don't hesitate to reach out to our friendly support team at support@opensouth.io

Best regards,
Open South. 

"""

    html = render_to_string(
        'email/dataset.html',
        {
            'content': f"""
You have been removed from the organisation {str(organisation.name).capitalize()}.
If you think this was an error or unintended, feel free to reach out to our support team""",
            'name' : str(user.first_name).title()

        }
    )

    send_email(
        recipient=user.email,
        subject="Open South - Organisation Removal",
        body=message,
        html=html
    )


def organisation_reject_users(user, organisation):

    message = f"""

Dear {str(user.first_name).capitalize()},

Your request to join the organisation {str(organisation.name).capitalize()} as been rejected.
If you think this was an error or unintended, feel free to reach out to our support team.

If you encounter any issues during the process or have any questions about our platform,
please don't hesitate to reach out to our friendly support team at support@opensouth.io

Best regards,
Open South.

"""
    html = render_to_string(
        'email/dataset.html',
        {
            'content': f"""
Your request to join the organisation {str(organisation.name).capitalize()} as been rejected.
If you think this was an error or unintended, feel free to reach out to our support team.""",
            'name' : str(user.first_name).title()

        }
    )

    send_email(
        recipient=user.email,
        subject="Open South - Organisation Request Declined",
        body=message,
        html=html
    )


def organisation_verification_email(email, user, organization, pin):

    message = f"""

Dear {str(user.first_name).capitalize()},

A new organization, {str(organization.name).capitalize()}, has been created.
Please use the following verification pin to verify your ownership:

Verification Pin: {pin}
If you have any questions or need assistance, please contact our support team at support@opensouth.io.
Best regards,
Open South.

"""
    html = render_to_string(
        'email/dataset.html',
        {
            'content': f""" A new organization, {str(organization.name).capitalize()}, has been created.
Please use the following verification pin to verify your ownership:

Verification Pin: {pin}

            """,
            'name' : str(user.first_name).title()

        }
    )
    
    send_email(
        recipient=email,
        subject="Open South - New Organisation Created",
        body=message,
        html=html
    )






def dataset_created_mail(email, user, message):

    body = f"""

Dear {str(user.first_name).capitalize()},

{message}

If you have any questions or need assistance, please contact our support team at support@opensouth.io.

Best regards,
Open South.

"""
    html = render_to_string(
        'email/dataset.html',
        {
            'content': str(message),
            'name' : str(user.first_name).title()

        }
    )
    
    send_email(
        recipient=email,
        subject="Open South - New Dataset Created",
        body=body,
        html=html
    )



   
def public_support_mail(to, name, message, address):

    body = f"""
Hello Admin

A new public support mail.

From: {str(name).capitalize()}

Address: {str(address).capitalize()}

Message: {str(message).capitalize()}


Best regards
Open South

"""
    send_email(
        recipient=to,
        subject="Open South - New Public Support Mail",
        body=body
    )
    

