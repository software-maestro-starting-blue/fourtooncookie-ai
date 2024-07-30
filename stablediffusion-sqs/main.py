from asyncio import sleep
import boto3
from dotenv import load_dotenv
import os
import glob
import base64
import json
from aws_sqs import receive_messages, delete_message, send_message
from sdxl_lora_runner import generate_image_sdxl_with_lora

load_dotenv()


def get_image_from_dir(diary_id, grid_position):
    folder_path = f"output/{diary_id}_{grid_position}"
    png_files = glob.glob(os.path.join(folder_path, '*.png'))
    if not png_files:
        return None
    
    with open(f"output/{diary_id}_{grid_position}/{png_files[0]}", 'rb') as f:
        image_bytes = f.read()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    os.remove(f"output/{diary_id}_{grid_position}/{png_files[0]}")
    return image_base64

def extract_message(message_body):
    message = json.loads(message_body)
    return message['diaryId'], message['characterId'], message['prompt'], message['gridPosition']

def run():
    while True:
        try:
            sleep(3) # 3초동안 대기

            messages = receive_messages()

            if not messages:
                continue

            for message_body, message_receipt_handle in messages:
                diary_id, character_id, prompt, grid_position = extract_message(message_body)

                lora_model = f"lora/model_{character_id}.safetensors"
                output_dir = f"output/{diary_id}_{grid_position}"

                generate_image_sdxl_with_lora(lora_model, prompt, output_dir)
                image_base64 = get_image_from_dir(diary_id, grid_position)

                send_message(diary_id, grid_position, image_base64)
                delete_message(message_receipt_handle)
        except Exception as e:
            print("An error occurred:", str(e))
            sleep(10)
            continue

if __name__ == '__main__':
    run()