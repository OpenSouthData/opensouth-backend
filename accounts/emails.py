from djoser.email import PasswordResetEmail
import os
import requests
from config.send_mail import send_email
from django.template.loader import render_to_string



key = os.getenv("email_key")





def requestotp_mail(email, otp, name):

    message = f"""

Dear {name},

To authenticate, please use the following One Time Password (OTP):

{otp}

Please do not share this OTP with anyone. At Open South, we take your account security very seriously. Our Support Team will never ask you to disclose or verify your password, OTP and other personal information. If you did not initiate this request, please contact our support team immediately.

If you encounter any issues during the verification process or have any questions about our platform, please do not hesitate to reach out to our friendly support team at support@opensouth.io.

Best regards,

Open South.

"""
    html = render_to_string('email/otp.html', {'name': name, 'code':otp})
    send_email(
        recipient=email,
        subject="OpenSouth - Request OTP",
        body=message,
        html=html
    )
 
   

   
def reset_password_mail(email, url, name):

    message = f"""

Dear {name},
If you need to change your password, no problem. Let us help you get a new one.



RESET PASSWORD: {url}


If you did not initiate this password reset or suspect that your account may have been accessed by someone else, please reach out to support@opensouth.io.
Best regards,
Open South.

"""
    html = render_to_string('email/change_password.html', {'name': name, 'url':url})
    send_email(
        recipient=email,
        subject="OpenSouth - Reset Password",
        body=message,
        html=html
    )

    




def login_mail(email, name):

    message = f"""

Dear {str(name).capitalize()},

You just logged in to your Open South account. If this was you, you can safely ignore this email. If you think someone else might have accessed your account, please contact our support team immediately.

If you have any questions or need assistance, please contact our support team at support@opensouth.io.

Best Regards,
Open South.


"""
    html = render_to_string(
        'email/login.html',
        {
            'content': f"""You just logged in to your Open South account. If this was you, you can safely ignore this email. If you think someone else might have accessed your account, please contact our support team immediately.""",
            'name' : str(name).title()

        }
    )
    send_email(
        recipient=email,
        subject="Open South - Login",
        body=message,
        html=html
        
        )