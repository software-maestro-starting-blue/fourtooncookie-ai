import subprocess

def generate_image_sdxl_with_lora(lora_model, prompt, output_dir):

    command = 'python3 sd-scripts/sdxl_gen_img.py --ckpt ./models/sd_xl_base_1.0_0.9vae.safetensors --outdir {} --xformers --bf16 --W 512 --H 512 --scale 7.0 --sampler dpmsolver++ --network_module networks.lora --network_weights {} --network_mul 1.0 --steps 70 --batch_size 1 --images_per_prompt 1 --prompt "{}"'.format(output_dir, lora_model, prompt)

    subprocess.run(command, shell=True)
