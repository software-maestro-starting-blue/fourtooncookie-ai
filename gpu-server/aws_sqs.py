import boto3
import os

sqs_client = boto3.client('sqs', region_name='ap-northeast-2')

SPRING_TO_STABLEDIFFUSION_QUEUE_URL= os.environ['SPRING_TO_STABLEDIFFUSION_QUEUE_URL']

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
            return None
        
        return [(message['Body'], message['ReceiptHandle']) for message in messages]
    
    except Exception as e:
        print("An error occurred while receiving messages:", str(e))
        return None


def delete_message(receipt_handle):
    try:
        sqs_client.delete_message(
            QueueUrl=SPRING_TO_STABLEDIFFUSION_QUEUE_URL,
            ReceiptHandle=receipt_handle
        )
        print("Deleted message from queue.")
    except Exception as e:
        print("An error occurred while deleting message:", str(e))
