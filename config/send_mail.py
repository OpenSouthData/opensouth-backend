import boto3
import os



session = boto3.Session(
    aws_access_key_id=os.getenv("mail_access_id"),
    aws_secret_access_key=os.getenv("mail_secret_key")
)

def send_email(subject, body, recipient, html=None):

    ses_client = session.client('ses', region_name=os.getenv("region"))

    message={

            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': body,
                    }
                },

            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject,
            }
        }
    
    if html:
        message['Body']['Html'] = {
            'Charset': 'UTF-8',
            'Data': html,
        }


    response = ses_client.send_email(

        Destination={
            'ToAddresses': [recipient],
        },

        Message=message,

        Source=os.getenv("email_from")
    )

    return response['ResponseMetadata']['HTTPStatusCode'] == 200

