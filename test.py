import os
import subprocess

# System Settings
systems = ["mac", "windows"]
system = systems[1]

# Experiment settings
times = 1 # How many times sampled
samples = 16 # How many samples
mode = "small"

data = open("data.csv", "a")
data.write("target,degrees\n")
data.close()

path_data = open("path_data.csv", "a")
path_data.write("target,nodes\n")

if system == systems[0]:
    command = ["cd", "~/Documents/Github/D3GREES/"]
    command1 = ["python3", "degrees.py", "small", f"{samples}"]
    subprocess.run(command)
    for i in range(times):
        subprocess.run(command1)
elif system == systems[1]:
    for i in range(times):
        os.popen(f"start cmd /k; cd C:\\Users\\26AiZavaleta\\OneDrive - St. Francis High School\\Documents\\GitHub\\D3GREES\\ ^& py degrees.py {mode} {samples}")

