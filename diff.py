import glob
import subprocess

for filename in glob.glob("./test/arm/kendrick/*.j"):
    with open(filename, "r") as f:
        file = f.read()
        result = subprocess.run(["python3", "compile.py"], input=file, capture_output=True)
        print(result)