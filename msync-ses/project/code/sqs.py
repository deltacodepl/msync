import boto3
import json
import os
import sys
import logging
# from jinja2 import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
# import multiprocessing
# import mypy_boto3_sesv2

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s %(module)s "
    "%(process)s[%(thread)s] %(message)s",
)

# QUEUE_URL: str = os.environ.get("QUEUE_URL")
# LAMBDA_RUN_TIME = 250000
# THRESHOLD = 100
CHARSET = 'UTF-8'
# THREAD_COUNT = 4
# SES_SEND_RATE = 14
REGION_NAME =  os.environ.get("REGION_NAME")

sqs_client = boto3.client(
    "sqs",
    region_name=REGION_NAME,
    # aws_access_key_id=os.environ.get("AWS_ACCESS_KEY"),
    # aws_secret_access_key=os.environ.get("AWS_SECRET_KEY"),
)
ses_client = boto3.client("ses", region_name=REGION_NAME)
s3_client = boto3.client("s3", region_name=REGION_NAME)


def mime_email(
    subject,
    from_address,
    to_address,
    cc_address=None,
    bcc_address=None,
    html_message=None,
):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_address
    msg["To"] = to_address
    if cc_address:
        msg["CC"] = cc_address
    if bcc_address:
        msg["BCC"] = bcc_address
    if html_message:
        msg.attach(MIMEText(html_message, "html"))

    return msg.as_string()


# def delete_sqs_message(recipt_handle)-> None:
#     sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=recipt_handle)


# def get_message()-> dict or None:
#     try:
#         response = sqs_client.receive_message(
#             QueueUrl=queue_url,
#             MaxNumberOfMessages=1,
#             WaitTimeSeconds=10,
#         )
#         print(response)
#         if len(response.get('Messages')) > 0:
#             return response.get('Messages')[0]
#         else:
#             return None
#     except Exception as e:
#         print(f"Error {e}")


# def process_message(message):
#     print(f"msg from SQS {message}")
#     delete_sqs_message(message['ReceiptHandle'])

def current_time() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())

def send_text_email(payload: dict):

    response = ses_client.send_email(
        Source= payload.get('from'),
        Destination={
            'ToAddresses': [
                payload.get('to'),
            ]
        },
        Message={
            'Subject': {
                'Data': payload.get('subject'),
                'Charset': CHARSET
            },
            'Body': {
                'Text': {
                    'Data': payload.get('result'),
                    'Charset': CHARSET
                }
            }
        }
    )

    return response


def send_email(payload: dict):
    try:
        response = ses_client.send_templated_email(
          Source=payload.get('from'),
          Destination={
            'ToAddresses': [
              payload.get('to')
            ],
            'CcAddresses': ['admin@'],
          },
          ReplyToAddresses=[
            payload.get('from'),
          ],
          Template='properline_email',
          TemplateData='{ \"username\":\"'+ payload.get('to') +'\", \"password\": \"'+ payload.get('password') +'\", \"host\": \"'+ payload.get('host') +'\", \"datetime\": \"'+ current_time() +'\" }'
        )
        
    except Exception as e:
        logger.error(f" SES error: {e}")
    else:
        logger.info(f"Email sent to: {payload.get('to')}")
        return response


def sqs(event, context):
    records = event['Records']

    for record in records:
        content = record['body']
        response = send_email(json.loads(content))
        logger.info(content)
        logger.info(response)

    return     {
        'statusCode': 200,
        'body': json.dumps(content)
    }

