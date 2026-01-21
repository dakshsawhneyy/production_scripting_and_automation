import subprocess
import boto3
import os
import requests
import logging
from datetime import date
from dotenv import load_dotenv

load_dotenv()

# Config
LOG_DIR = "/var/log/myapp/" # Be specific, don't scan all of /var/log!
BUCKET_NAME = "daksh-ops-archive"
SLACK_URL = os.getenv('SLACK_URL')
REGION = "ap-south-1"

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def get_stale_files():
    # Find files > 3 days old
    cmd = ["find", LOG_DIR, "-type", "f", "-name", "*.log", "-mtime", "+3"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if not result.stdout.strip():
        return []
        
    return result.stdout.strip().split('\n') # <--- KEY FIX: Split into list

def compress_file(filepath):
    """Compresses file and returns the new path"""
    # gzip -f forces compression even if file exists
    subprocess.run(["gzip", "-f", filepath], check=True)
    return f"{filepath}.gz"

def send_report(count, saved_mb):
    if not SLACK_URL: return
    
    payload = {
        "text": f"🧹 Log Cleanup Report:\n- Archived: {count} files\n- Space Freed: {saved_mb:.2f} MB"
    }
    try:
        requests.post(SLACK_URL, json=payload, timeout=5)
    except Exception as e:
        logging.error(f"Slack failed: {e}")

# --- Main Execution ---
try:
    s3 = boto3.client('s3', region_name=REGION)
    files_to_process = get_stale_files()
    
    total_files = 0
    total_size_bytes = 0

    print(f"found {len(files_to_process)} stale files.")

    for log_file in files_to_process:
        if not log_file: continue
        
        try:
            # 1. Calculate size BEFORE compression (This is the space we are freeing)
            original_size = os.path.getsize(log_file)
            
            # 2. Compress (Original is replaced by .gz)
            gz_file = compress_file(log_file)
            logging.info(f"Compressed: {gz_file}")
            
            # 3. Upload
            s3_key = f"logs/{date.today()}/{os.path.basename(gz_file)}"
            s3.upload_file(gz_file, BUCKET_NAME, s3_key)
            logging.info(f"Uploaded: {s3_key}")
            
            # 4. Verify & Destroy (Delete the .gz file)
            os.remove(gz_file)
            logging.info(f"Deleted local: {gz_file}")
            
            # 5. Update Metrics
            total_files += 1
            total_size_bytes += original_size

        except Exception as e:
            logging.error(f"Failed to process {log_file}: {e}")

    # Final Report
    if total_files > 0:
        size_mb = total_size_bytes / (1024 * 1024)
        send_report(total_files, size_mb)
        print("✅ Job Complete.")

except Exception as e:
    logging.critical(f"Script crashed: {e}")