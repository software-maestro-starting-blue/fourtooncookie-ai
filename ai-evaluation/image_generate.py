import subprocess

'''
SETTING
'''
SDXL_MODEL_PATH = "./"

LORA_MODEL_PATH = "./"

OUTPUT_DIR = "./output"

prompts = [
    "example"
]

muls = [
    1.0,
    0.9
]

STEPS = 70

IMAGES_PER_PROMPT_AND_MUL = 100

'''
END OF SETTING
'''

def generate_image_sdxl_with_lora(prompt, mul, output_dir):

    command = f'python3 sd-scripts/sdxl_gen_img.py --ckpt {SDXL_MODEL_PATH} --outdir {output_dir} --xformers --bf16 --W 512 --H 512 --scale 7.0 --sampler dpmsolver++ --network_module networks.lora --network_weights {LORA_MODEL_PATH} --network_mul {mul} --steps {STEPS} --batch_size 1 --images_per_prompt {IMAGES_PER_PROMPT_AND_MUL} --prompt "{prompt}"'

    subprocess.run(command, shell=True)

for prompt in prompts:
    for mul in muls:
        output_dir = OUTPUT_DIR + "/" + prompt + "_" + str(mul)
        with open(output_dir + "/describe.txt", "w") as f:
            f.write(f"Generated image \nprompt: {prompt} \nmul: {mul}")
        
        print(f"Generating image for prompt: {prompt} with mul: {mul}")
        generate_image_sdxl_with_lora(prompt, mul, output_dir)
        
