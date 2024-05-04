import requests
import os


key = os.getenv("email_key")








def organisation_actions_mail(user, message, action):

    
    requests.post(
        url="https://api.useplunk.com/v1/send",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        },

        json={
            "to": user.email,
            "subject": f"Open South - Organisation {str(action).capitalize()}",
            "body": f"""
            <html>
                <body>
                    <p>Dear {str(user.first_name).capitalize()},</p>

                    <p> {message}</p>

                    <p>If you have any questions or need assistance, please contact our support team at support@opensouth.io.</p>
                    <p>Best regards,</p>
                    <p>Open South.</p>
                </body>
            </html>
            """
        }
    )


def dataset_actions_mail(user, message, action):

    
    requests.post(
        url="https://api.useplunk.com/v1/send",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        },

        json={
            "to": user.email,
            "subject": f"Open South - Dataset {str(action).capitalize()}",
            "body": f"""
            <html>
                <body>
                    <p>Dear {str(user.first_name).capitalize()},</p>

                    <p> {message}</p>

                    <p>If you have any questions or need assistance, please contact our support team at support@opensouth.io.</p>
                    <p>Best regards,</p>
                    <p>Open South.</p>
                </body>
            </html>
            """
        }
    )



