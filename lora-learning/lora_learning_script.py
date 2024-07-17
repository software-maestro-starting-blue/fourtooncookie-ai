import subprocess


def start_lora_learning(args):
    command = "accelerate launch --num_cpu_threads_per_process 1 train_network.py"

    for key, value in args.items():
        command += "\n --{} {}".format(key, value)

    subprocess.run(command, cwd="./sd-scripts")