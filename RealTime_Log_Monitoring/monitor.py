import sys
import re

# sys.stdin is used for reading input piped from another program
for line in sys.stdin:
    status_code_re = re.search(r'\" (\d{3})', line)     # Look for " then ' '[space] then \d means digit(0-9) with len 3
    ip_address_re = re.search(r'(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}) ', line)
    status_code = int(status_code_re.group(1))
    ip_address = ip_address_re.group(1)
    print(ip_address)
    if status_code == 500 or status_code == 404:
        print(f"🚨 CRITICAL ALERT: {status_code} Error Detected!")
    else:
        print(f"Traffic Normal {status_code}")