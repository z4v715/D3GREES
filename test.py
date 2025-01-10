import os
import subprocess
import random
import csv

import time

def random_samples(times, spread):
    for i in range(times):

        ids = list()

        with open(f"{mode}/people.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ids.append(row["id"])

        source = ids[random.randint(1, spread - 1)]
        target = ids[random.randint(1, spread - 1)]

        start = time.time()

        os.popen(f"start cmd /k; cd C:\\Users\\26AiZavaleta\\OneDrive - St. Francis High School\\Documents\\GitHub\\D3GREES\\ ^& py degrees.py {mode} {source} {target} ^& exit")

        end = time.time()

        time_complexity = open("timed.csv", "a")
        time_complexity.write(f"{source},{target},{spread},{end - start}\n")
        time_complexity.close()


# System Settings
systems = ["mac", "windows"]
system = systems[1]

# Experiment settings
samples = 5 # How many times sampled
deviation = 16 # Up to what number of actors can be chosen
mode = "small"

data = open("data.csv", "a")
data.write("source,target,degrees\n")
data.close()

path_data = open("path_data.csv", "a")
path_data.write("source,target,nodes\n")
path_data.close()

time_complexity = open("timed.csv", "a")
time_complexity.write(f"source,target,deviation,time\n")
time_complexity.close()

if system == systems[0]:
    command = ["cd", "~/Documents/Github/D3GREES/"]
    command1 = ["python3", "degrees.py", "small", f"{samples}"]
    subprocess.run(command)
    for i in range(samples):
        subprocess.run(command1)

elif system == systems[1]:
    random_samples(samples, deviation)