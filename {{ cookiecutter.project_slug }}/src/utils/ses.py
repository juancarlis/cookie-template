from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import boto3
from botocore.client import ClientError


class EMailController:

    @staticmethod
    def send_email(sender, destination, subject, message):
        client = boto3.client('ses', 'us-east-1')
        response = client.send_email(
            Source=sender,
            Destination={
                'ToAddresses': destination
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': message
                    },
                    'Html': {
                        'Data': message
                    }
                }
            },
            ReplyToAddresses=[
                sender
            ]
        )

        return response

    @staticmethod
    def send_email_with_s3_attachment(sender, destination, body, subject, bucketname, file_path):
        # Text part
        msg = MIMEMultipart()
        part = MIMEText(body, _subtype='html')
        msg.attach(part)

        filename = file_path.split('/')[-1]
        s3_file_path = file_path.replace(bucketname, '')

        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = destination

        # File part
        s3_object = boto3.client('s3')
        s3_object = s3_object.get_object(Bucket=bucketname, Key=s3_file_path)
        file = s3_object['Body'].read().decode('utf-8-sig')

        part = MIMEApplication(file, filename)
        part.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(part)

        client = boto3.client('ses', 'us-east-1')

        try:
            result = client.send_raw_email(
                    RawMessage={'Data': msg.as_bytes()}
                    )
            return (
                    {'message': 'error', 'status': 'fail'}
                    if 'ErrorResponse' in result 
                    else {'message': 'email sent successfully', 'status': 'success'}
                    )
        except ClientError as e:
            return (
                    {'message': e.response['Error']['Message'], 
                        'status': 'fail'}
                    )

        except AttributeError as e:
            return  (
                    {'message': 'no utilizar listas en los parámetros del correo',
                        'status': 'fail'}
                    ) 
