import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

BATCH_RESULT_FOLDER_PATH = "./"

def process_batch(batch_job_id):
    if os.path.isfile(os.path.join(BATCH_RESULT_FOLDER_PATH, batch_job_id + ".jsonl")):
        print(f"Batch job {batch_job_id} already processed")
        return True

    response = client.batches.retrieve(batch_job_id)

    status = response["status"]

    if status == "failed" or status == "expired" or status == "cancelled" or status == "completed":
        print(f"Batch job {batch_job_id} finished")
        output_file_id = response["output_file_id"]
        result = client.files.content(output_file_id)
        with open(os.path.join(BATCH_RESULT_FOLDER_PATH, batch_job_id + ".jsonl"), "w") as f:
            f.write(result.text)
    else:
        return False

def process_all_batches():
    batches = client.batches.list(limit=10, after=None)

    left_batch_ids = []

    for batch in batches:
        batch_job_id = batch.id
        if not process_batch(batch_job_id):
            left_batch_ids.append(batch_job_id)
    
    return left_batch_ids

def process_left_batches(batch_ids):
    left_batch_ids = []

    for batch_id in batch_ids:
        if not process_batch(batch_id):
            left_batch_ids.append(batch_id)
    
    return left_batch_ids

if __name__ == "__main__":

    # 모든 batch 처리
    left_batch_ids = process_all_batches()
    while True:
        
        left_batch_ids = process_all_batches(left_batch_ids)

        if not left_batch_ids:
            break
