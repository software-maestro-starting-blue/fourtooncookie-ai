from asyncio import sleep
import os
import glob
import json
from aws_sqs import receive_messages, delete_message
from aws_s3 import upload_image_to_s3
from sdxl_lora_runner import generate_image_sdxl_with_lora
import sentry_sdk

sentry_sdk.init(
    dsn=os.environ['SENTRY_DSN'],
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


def extract_message(message_body):
    message = json.loads(message_body)
    return message['diaryId'], message['characterId'], message['prompt'], message['gridPosition']

def get_image_path(diary_id, grid_position):
    folder_path = f"output/{diary_id}_{grid_position}"
    png_files = glob.glob(os.path.join(folder_path, '*.png'))
    if not png_files:
        return None
    
    return f"./output/{diary_id}_{grid_position}/{png_files[0]}"

def delete_output_images():
    for file in glob.glob('output/*'):
        os.remove(file)

def run():
    while True:
        sleep(3) # 3초동안 대기

        messages = receive_messages()

        if not messages:
            continue

        for message_body, message_receipt_handle in messages:
            diary_id, character_id, prompt, grid_position = extract_message(message_body)

            lora_model = f"lora/model_{character_id}.safetensors"
            output_dir = f"output/{diary_id}_{grid_position}"

            generate_image_sdxl_with_lora(lora_model, prompt, output_dir)
            image_path = get_image_path(diary_id, grid_position)

            upload_image_to_s3(image_path, diary_id, grid_position)

            delete_message(message_receipt_handle)

if __name__ == '__main__':
    try:
        run()
    except KeyboardInterrupt as e:
        print("Shutting down...")
    except Exception as e:
        print("An error occurred:", str(e))
        sentry_sdk.capture_exception(e)
    finally:
        delete_output_images()