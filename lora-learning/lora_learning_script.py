import subprocess
import toml
import os

NOW_PATH = os.path.abspath('.') + "/"

ACCELERATE_PATH = NOW_PATH + "venv/bin/accelerate"
NETWORK_PATH = NOW_PATH + "sd-scripts/sdxl_train_network.py"
OUTPUTS_PATH = NOW_PATH + "outputs/"

DEFAULT_MODEL_PATH = NOW_PATH + "model/sd_xl_base_1.0_0.9vae.safetensors"
DEFAULT_CONFIG_PATH = NOW_PATH + "defaults/default_config.toml"

def learn_lora_model(model_name: str,
                     
                     epoch: int = 1,
                     gradient_accumulation_steps: int = 1,
                     train_batch_size: int = 1,

                     learning_rate: float = 0.0001,
                     text_encoder_lr: float = 0.0001,
                     unet_lr: float = 0.0001,

                     network_dim: int = 8,
                     network_alpha: int = 8,

                     rank_dropout: float = 0,
                     module_dropout: float = 0,
                     network_dropout: float = 0,

                     optimizer_type: str = "AdamW",

                     pretrained_model_path: str = DEFAULT_MODEL_PATH):
    config = toml.load(DEFAULT_CONFIG_PATH)

    img_path = OUTPUTS_PATH + model_name + "/img"
    model_path = OUTPUTS_PATH + model_name + "/model"
    log_path = OUTPUTS_PATH + model_name + "/log"

    # 학습 저장 디렉토리 생성
    os.makedirs(img_path, exist_ok=True)
    os.makedirs(model_path, exist_ok=True)
    os.makedirs(log_path, exist_ok=True)

    # prompt.txt 생성   
    with open(model_path + "/prompt.txt", "w") as f:
        f.write("")
        f.close()

    # 학습 데이터 수 계산
    img_folders = os.listdir(img_path)
    train_steps = 0
    for folder in img_folders:
        repeat = folder.split("_")[0]
        img_files = os.listdir(img_path + "/" + folder)
        max_train_steps += img_files.count("png") * repeat
    
    config["max_train_steps"] = int(train_steps / train_batch_size / gradient_accumulation_steps * epoch)
    config["lr_warmup_steps"] = int(config["max_train_steps"] * 0.1)

    # CONFIG 설정 및 저장

    config["logging_dir"] = OUTPUTS_PATH + model_name + "/log"
    config["output_dir"] = OUTPUTS_PATH + model_name + "/model"
    config["sample_prompts"] = OUTPUTS_PATH + model_name + "/model/prompt.txt"
    config["train_data_dir"] = OUTPUTS_PATH + model_name + "/img"
    config["pretrained_model_name_or_path"] = pretrained_model_path

    config["output_name"] = model_name

    config["epoch"] = epoch
    config["gradient_accumulation_steps"] = gradient_accumulation_steps
    config["train_batch_size"] = train_batch_size

    config["learning_rate"] = learning_rate
    config["text_encoder_lr"] = text_encoder_lr
    config["unet_lr"] = unet_lr

    config["network_dim"] = network_dim
    config["network_alpha"] = network_alpha

    config["network_args"] = ["rank_dropout={}".format(rank_dropout), "module_dropout={}".format(module_dropout)]
    config["network_dropout"] = network_dropout
    config["optimizer_type"] = optimizer_type
    
    config_path = OUTPUTS_PATH + model_name + "/config.toml"
    with open(config_path, "w") as f:
        toml.dump(config, f)
        f.close()
    
    
    # 학습 시작
    args = [
        ACCELERATE_PATH, "launch",
        "--dynamo_backend", "no",
        "--dynamo_mode" , "default", 
        "--mixed_precision" , config["mixed_precision"],
        "--num_processes" , "1",
        "--num_machines" , "1",
        "--num_cpu_threads_per_process" , "2",
        NETWORK_PATH,
        "--config_file" , config_path
    ]

    subprocess.run([" ".join(args)], shell=True)