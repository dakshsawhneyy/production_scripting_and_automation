import requests
import json
import sys
import re
import os
from dotenv import load_dotenv

load_dotenv()
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

def send_alert(severity, error_code):
    
    payload = {
        "text": f"Server Error {error_code}",
        "severity": severity
    }
    
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        print("Error Occurred", e)
    
# Passing input to this script sys.stdin
for line in sys.stdin:
    
    line = line.strip()
    if not line: continue
    
    match = re.search(r'\" (\d{3})')
    if match:
        status_code = int(match.group(1))
        if status_code >= 400 and status_code < 600:
            severity = "High"
            send_alert(severity, status_code)