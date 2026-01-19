import psutil
import time

while True:
    cpu = int(psutil.cpu_percent(interval=1))
    memory = int(psutil.virtual_memory().percent)
    
    if cpu > 80 or memory > 80:
        print(f"🔥 HIGH LOAD ALERT! CPU: {cpu}%, RAM: {memory}%")
    else:
        print(f"System Normal: CPU: {cpu}%, RAM: {memory}%")
        
    time.sleep(5)