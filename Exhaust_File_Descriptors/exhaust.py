import os
import time

filename = "./exhaust.py"

opened = []
try:
    for i in range(2000):
        f = open(filename, "r")
        opened.append(f)
        print(f"Opened File -- {i}")
except Exception as e:
    print(f"Crashed at {i}")
    print("Error Occurred", e)
    time.sleep(20)