import os
from PIL import Image
import base64
from mimetypes import guess_type
import json

from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

BATCH_JSONL_FILE_NAME = "batch_datas.jsonl"
BATCH_JOB_JSON_FILE_NAME = "batch_job.json"
EVALUATION_SYSTEM_PROMPT = '''
You can write a description of the image or ask a question about it.
'''

def process_txt_file(file_path):
    """txt 파일을 읽어서 prompt와 mul 값을 추출하는 함수"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
        # txt 파일 내용에서 prompt와 mul 값 추출
        prompt = None
        mul = None
        
        for line in lines:
            if line.startswith("prompt:"):
                prompt = line.split("prompt:")[1].strip()
            elif line.startswith("mul:"):
                mul_str = line.split("mul:")[1].strip()

                try:
                    mul = float(mul_str)
                except ValueError:
                    print(f"mul 값을 float으로 변환할 수 없어요: {mul_str}")
                    mul = None  # 변환 실패 시 None 또는 기본값 처리
        
        # 추출된 값들을 dict로 리턴
        processed_data = {
            "prompt": prompt,
            "mul": mul
        }
        
        print(f"Processed TXT file: {file_path}")
        print(f"Extracted prompt: {prompt}")
        print(f"Extracted mul: {mul}")
        
        return processed_data

def local_image_to_data_url(image_path):
    # Guess the MIME type of the image based on the file extension
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # Default MIME type if none is found

    # Read and encode the image file
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Construct the data URL
    return f"data:{mime_type};base64,{base64_encoded_data}"

def process_png_file(file_path, config_data):
    """png 파일을 config 파일의 데이터를 활용하여 처리하는 함수"""
    data_url = local_image_to_data_url(file_path)
    prompt = config_data["prompt"]
    mul = config_data["mul"]

    return {
        "custom_id": f"task-{prompt}-{mul}-{file_path}",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            # This is what you would have in your Chat Completions API call
            "model": "gpt-4o",
            "temperature": 1,
            "response_format": { 
                "type": "json_object"
            },
            "messages": [
                {
                    "role": "system",
                    "content": EVALUATION_SYSTEM_PROMPT
                },
                { 
                    "role": "user", 
                    "content": [{"type": "image_url", "image_url": {"url": data_url}}]
                }
            ],
        }
    }

def process_folder(folder_path):
    """하위 폴더의 txt 파일을 읽고, png 파일을 처리하는 함수"""
    txt_file_path = None
    png_files = []

    is_processed = False

    # 하위 폴더 내의 모든 파일을 확인하여 txt 파일과 png 파일을 구분
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if file_name.endswith(".txt"):
            txt_file_path = file_path  # txt 파일 경로 저장
        
        elif file_name.endswith(".png"):
            png_files.append(file_path)  # png 파일 경로 리스트에 저장
        
        elif file_name == BATCH_JOB_JSON_FILE_NAME:
            is_processed = True
    
    # 이미 처리된 폴더인 경우 처리하지 않음
    if is_processed:
        print(f"Folder {folder_path} already processed")
        return

    if txt_file_path is None or len(png_files) == 0:
        return
    
    # txt 파일을 읽어 필요한 정보를 가공 (config 역할)
    config_data = process_txt_file(txt_file_path)
    
    # 가공한 정보를 활용해 png 파일들로 task 생성
    tasks = []
    for png_file in png_files[:1]:
        tasks.append(process_png_file(png_file, config_data))

    # batch_datas.jsonl 파일 생성
    batch_datas_file_name = os.path.join(folder_path, BATCH_JSONL_FILE_NAME)
    with open(batch_datas_file_name, "w") as f:
        for task in tasks:
            f.write(json.dumps(task) + "\n")
    batch_file = client.files.create(
        file=open(batch_datas_file_name, "rb"),
        purpose="batch"
    )
    batch_job = client.batches.create(
        input_file_id=batch_file.id,
        endpoint="/v1/chat/completions",
        completion_window="24h"
    )
    
    # batch_job_id를 파일로 저장
    batch_job_file_name = os.path.join(folder_path, BATCH_JOB_JSON_FILE_NAME)
    with open(batch_job_file_name, "w") as f:
        f.write(json.dumps({
            "batch_job_id": batch_job.id
        }))
    
    print(f"Folder {folder_path} processed")

def process_all_folders(root_folder):
    """최상위 폴더 내의 모든 하위 폴더를 처리하는 함수"""
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        
        if os.path.isdir(folder_path):
            process_folder(folder_path)

if __name__ == "__main__":
    # 최상위 폴더 경로 설정
    root_folder = "./"
    
    # 모든 하위 폴더 처리
    process_all_folders(root_folder)
