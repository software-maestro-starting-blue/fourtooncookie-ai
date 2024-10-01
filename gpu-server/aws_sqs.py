import boto3
import os
from dotenv import load_dotenv

load_dotenv()

sqs_client = boto3.client('sqs', region_name='ap-northeast-2')

SPRING_TO_STABLEDIFFUSION_QUEUE_URL= os.environ.get('SPRING_TO_STABLEDIFFUSION_SQS_URL')
STABLEDIFFUSION_TO_SPRING_QUEUE_URL = os.environ.get('STABLEDIFFUSION_TO_SPRING_SQS_URL')

NUMBER_OF_MESSAGES_TO_RECEIVE = 5


def receive_messages():
    try:
        response = sqs_client.receive_message(
            QueueUrl=SPRING_TO_STABLEDIFFUSION_QUEUE_URL,
            MaxNumberOfMessages=NUMBER_OF_MESSAGES_TO_RECEIVE,
            WaitTimeSeconds=20
        )
    
        messages = response.get('Messages', [])
    
        if not messages:
            print("No messages received.")
            return None, None
        
        return [(message['Body'], message['ReceiptHandle']) for message in messages]
    
    except Exception as e:
        print("An error occurred while receiving messages:", str(e))
        return None, None


def delete_message(receipt_handle):
    try:
        sqs_client.delete_message(
            QueueUrl=SPRING_TO_STABLEDIFFUSION_QUEUE_URL,
            ReceiptHandle=receipt_handle
        )
        print("Deleted message from queue.")
    except Exception as e:
        print("An error occurred while deleting message:", str(e))
