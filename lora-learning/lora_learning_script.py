import subprocess

args = {}

command = "accelerate launch --num_cpu_threads_per_process 1 train_network.py"

for key, value in args.items():
    command += "\n --{} {}".format(key, value)

subprocess.run(command)