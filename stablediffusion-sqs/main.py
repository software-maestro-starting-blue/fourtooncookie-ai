import boto3
import os
import glob
from aws_sqs import receive_message, delete_message, send_message
from sdxl_lora_runner import generate_image_sdxl_with_lora

sqs_client = boto3.client('sqs', region_name='us-east-1',
                          aws_access_key_id='',
                          aws_secret_access_key='')

springtosd_queue_url = ''
sdtospring_queue_url = ''

def get_image_from_dir(diary_id, grid_position):
    folder_path = f"output/{diary_id}_{grid_position}"
    png_files = glob.glob(os.path.join(folder_path, '*.png'))
    if len(png_files) == 0:
        return None
    
    with open(f"output/{diary_id}_{grid_position}/{png_files[0]}", 'rb') as f:
        return f.read()


def run():
    while True:
        message, receipt_handle = receive_message()

        if not message:
            continue

        diary_id = message['diary_id']
        character = message['character']
        prompt = message['prompt']
        grid_position = message['grid_position']

        lora_model = f"lora/model_{character}.safetensors"
        output_dir = f"output/{diary_id}_{grid_position}"

        generate_image_sdxl_with_lora(lora_model, prompt, output_dir)
        image = get_image_from_dir(diary_id, grid_position)

        send_message(diary_id, grid_position, image)
        delete_message(receipt_handle)

if __name__ == '__main__':
    run()