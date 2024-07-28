import boto3

sqs_client = boto3.client('sqs', region_name='us-east-1',
                          aws_access_key_id='',
                          aws_secret_access_key='')

springtosd_queue_url = ''
sdtospring_queue_url = ''

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
        MessageBody={
            'diary_id': diary_id,
            'grid_position': grid_position,
            'image': image
        }
    )