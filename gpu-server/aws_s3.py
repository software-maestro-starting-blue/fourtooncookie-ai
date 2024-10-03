import boto3
import os

s3_client = boto3.client('s3', region_name='ap-northeast-2')

S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']

def get_s3_image_path(diary_id, grid_position):
    return f"{diary_id}/{grid_position}.png"

def upload_image_to_s3(local_file_path, diary_id, grid_position):
    s3_image_path = get_s3_image_path(diary_id, grid_position)
    try:
        s3_client.upload_file(local_file_path, S3_BUCKET_NAME, s3_image_path)
        print("Uploaded image to S3.")
    except Exception as e:
        print("An error occurred while uploading image to S3:", str(e))
        raise e