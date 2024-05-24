from config.send_mail import send_email
from django.template.loader import render_to_string
import os






def partners_request_mail(data):

    message = f"""
    
Dear Admin,
         {str(data['organisation_name']).title()} has requested to be a partner with Open South.

         Email: {data['email']}
         Phone: {data['phone']}
         Description: {data['description']}
         Organisaton Type: {data['organisation_type']}

         Please review the request and approve or decline it.

Best regards,
Open South.

"""
    html = render_to_string(
        'email/partners.html',
        {   'content': f"""

Dear Admin,
         {str(data['organisation_name']).title()} has requested to be a partner with Open South.

         Email: {data['email']}
         Phone: {data['phone']}
         Description: {data['description']}
         Organisaton Type: {data['organisation_type']}

         Please review the request and approve or decline it.

Best regards,
Open South.

""",

        }
    )
    send_email(
        recipient=os.getenv("email_from"),
        subject="Open South - Partners Request",
        body=message,
        html=html
    )

   