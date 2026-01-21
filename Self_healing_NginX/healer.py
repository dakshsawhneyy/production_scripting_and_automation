import subprocess
import requests
import logging
from dotenv import load_dotenv
import os
import time

load_dotenv()

SLACK_URL=os.getenv("SLACK_URL")

logging.basicConfig(
    filename='nginx_status.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def send_msg_to_slack():
    message = f"Nginx server restarted at {time.time()}"
    requests.post(SLACK_URL, message)
    logging.info("Slack Message sent successfully")

while True:
    result = subprocess.run(["systemctl", "is-active", "nginx"], text=True, capture_output=True)
    if result.returncode != 0:
        print("NginX is dead. Restarting nginx")
        logging.critical(f"Nginx is down at {time.time()}")
        subprocess.run(["systemctl", "restart", "nginx"], text=True, capture_output=True)
        logging.info("Restarted NginX")
        send_msg_to_slack()
    else:
        logging.info(f"NginX running perfectly at {time.time()}")
    time.sleep(10)