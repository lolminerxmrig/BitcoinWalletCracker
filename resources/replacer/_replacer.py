import glob

for file in glob.glob("*.txt"):
    with open(file) as f:
        data = f.read().replace('\n', ' ')
    with open(file, "w") as f:
        f.write(data)
