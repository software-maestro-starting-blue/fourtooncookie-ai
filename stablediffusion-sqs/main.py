import boto3
from dotenv import load_dotenv
import os
import glob
from aws_sqs import receive_message, delete_message, send_message
from sdxl_lora_runner import generate_image_sdxl_with_lora
import base64

load_dotenv()


def get_image_from_dir(diary_id, grid_position):
    folder_path = f"output/{diary_id}_{grid_position}"
    png_files = glob.glob(os.path.join(folder_path, '*.png'))
    if len(png_files) == 0:
        return None
    
    with open(f"output/{diary_id}_{grid_position}/{png_files[0]}", 'rb') as f:
        image_bytes = f.read()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        return image_base64


def run():
    while True:
        message, receipt_handle = receive_message()

        if not message:
            continue

        diary_id = message['diaryId']
        character_id = message['characterId']
        prompt = message['prompt']
        grid_position = message['gridPosition']

        lora_model = f"lora/model_{character_id}.safetensors"
        output_dir = f"output/{diary_id}_{grid_position}"

        generate_image_sdxl_with_lora(lora_model, prompt, output_dir)
        image_base64 = get_image_from_dir(diary_id, grid_position)

        send_message(diary_id, grid_position, image_base64)
        delete_message(receipt_handle)

if __name__ == '__main__':
    run()