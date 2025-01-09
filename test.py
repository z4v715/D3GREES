import os
import subprocess
import csv

systems = ["mac", "windows"]
system = systems[0]
times = 1
samples = 600

data = open("data.csv", "a")
data.write("target,degrees\n")
data.close()

if system == systems[0]:
    command = ["cd", "~/Documents/Github/D3GREES/"]
    command1 = ["python3", "degrees.py", "large", f"{samples}"]
    subprocess.run(command)
    for i in range(times):
        subprocess.run(command1)
elif system == systems[1]:
    for i in range(times):
        os.popen("start cmd /k; cd C:\\Users\\26AiZavaleta\\OneDrive - St. Francis High School\\Documents\\GitHub\\D3GREES\\ ^& python degrees.py small ^&exit")

formatted = open("formatted_data.csv", "a")
formatted.write("target,degrees\n")

names = dict()

with open("data.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["target"] not in names.keys():
            names[row["target"]] = f"{row["degrees"]} "
        else:
            names[row["target"]] += f"{row["degrees"]} "

for item in names.items():
    formatted.write(f"{item[0]},{item[1]}\n")
