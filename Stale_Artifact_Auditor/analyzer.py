import subprocess
import os
import json

raw_file = "./raw_targets.txt"
json_file = "./outputs.json"

if not os.path.exists(raw_file):
    print("raw paths file didn't found")
    exit(1)

data_list = []

with open(raw_file, "r") as f:
    for line in f:
        clean_path = line.strip()
        if clean_path and os.path.exists(clean_path):
            
            raw = subprocess.run(["du", "-sk", clean_path], capture_output=True, text=True)
            result = raw.stdout.strip()

            payload = {
                "filepath": result.split()[1],
                "size": result.split()[0]
            }
            
            data_list.append(payload)
            
# Create a JSON File and put name and size into that
# if os.path.exists(json_file) and os.path.getsize(json_file) >= 0:
#     with open(json_file, "r") as f:
#         try:
#             data = json.load(f)    
#         except json.JSONDecodeError:
#             data = []
    
#         data.extend(data_list)
    
#         with open(json_file, "w") as fi:
#             fi.write(json.dumps(data, indent=4))

# OverWrite Mode
with open(json_file, "w") as f:
    json.dump(data_list, f, indent=4)