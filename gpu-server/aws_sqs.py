import boto3
import os
import json

sqs_client = boto3.client('sqs', region_name='ap-northeast-2')

SPRING_TO_STABLEDIFFUSION_QUEUE_URL= os.environ['SPRING_TO_STABLEDIFFUSION_QUEUE_URL']
IMAGE_RESPONSE_QUEUE_URL = os.environ['IMAGE_RESPONSE_QUEUE_URL']

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
        raise e


def send_image_success_message(diary_id: int, grid_position: int):
    try:
        sqs_client.send_message(
            QueueUrl=IMAGE_RESPONSE_QUEUE_URL,
            MessageBody=json.dumps({
                'diaryId': diary_id,
                'gridPosition': grid_position,
                'status': True
            })
        )
        print("Sent image success message to queue.")
    except Exception as e:
        print("An error occurred while sending image success message:", str(e))
        raise e


def send_image_failure_message(diary_id: int, grid_position: int):
    try:
        sqs_client.send_message(
            QueueUrl=IMAGE_RESPONSE_QUEUE_URL,
            MessageBody=json.dumps({
                'diaryId': diary_id,
                'gridPosition': grid_position,
                'status': False
            })
        )
        print("Sent image failure message to queue.")
    except Exception as e:
        print("An error occurred while sending image failure message:", str(e))
        raise e