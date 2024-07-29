import boto3
import os
from dotenv import load_dotenv
import json

load_dotenv()

sqs_client = boto3.client('sqs', region_name='ap-northeast-2',
                          aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

springtosd_queue_url = os.environ.get('SPRING_TO_STABLEDIFFUSION_SQS_URL')
sdtospring_queue_url = os.environ.get('STABLEDIFFUSION_TO_SPRING_SQS_URL')


def receive_message():
    response = sqs_client.receive_message(
            QueueUrl=springtosd_queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20
        )

    messages = response.get('Messages', [])

    if not messages:
        print("No messages received.")
        return False

    for message in messages:
        receipt_handle = message['ReceiptHandle']
        body = message['Body']

        return body, receipt_handle


def delete_message(receipt_handle):
    sqs_client.delete_message(
        QueueUrl=springtosd_queue_url,
        ReceiptHandle=receipt_handle
    )
    print("Deleted message from queue.")



def send_message(diary_id, grid_position, image):
    print("Sending image to Spring.")
    sqs_client.send_message(
        QueueUrl=sdtospring_queue_url,
        MessageBody=json.dumps({
            'diaryId': diary_id,
            'gridPosition': grid_position,
            'image': image
        }),
        MessageGroupId="reply"
    )