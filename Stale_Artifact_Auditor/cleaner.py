import argparse
import json
import os
import shutil

json_file = "./outputs.json"

# Adding Argument
parser = argparse.ArgumentParser()
parser.add_argument("--dry-run", required=False, action="store_true")
args = parser.parse_args()

if os.path.exists(json_file):
    with open(json_file, "r") as f:
        data = json.load(f)
        
        for indv_data in data:
            if args.dry_run:
                print(f"deleting file {indv_data['filepath']}")
            else:
                print(f"permanently deleting file {indv_data['filepath']}")
                try:
                    shutil.rmtree(indv_data['filepath'])
                except Exception as e:
                    print("Error Occurred", e)