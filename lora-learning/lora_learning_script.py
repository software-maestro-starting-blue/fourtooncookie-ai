import subprocess

NOW_PATH = "./"

ACCELERATE_PATH = NOW_PATH + "venv/bin/accelerate"
NETWORK_PATH = NOW_PATH + "sd-scripts/sdxl_train_network.py"
CONFIG_PATH = NOW_PATH + "outputs/training9/model/config_lora-20240720-0303.toml"

args = [
    ACCELERATE_PATH , "launch",
    "--dynamo_backend" , "no",
    "--dynamo_mode" , "default", 
    "--mixed_precision" , "fp16", 
    "--num_processes" , 1, 
    "--num_machines" , 1, 
    "--num_cpu_threads_per_process" , 2,
    NETWORK_PATH,
    "--config_file" , CONFIG_PATH
]

subprocess.run(args, shell=True)