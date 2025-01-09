import csv

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

formatted.close()