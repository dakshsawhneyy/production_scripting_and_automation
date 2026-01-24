import boto3
from datetime import datetime, timedelta, timezone
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def check_is_production(tags):
    """
    Returns True if the instance has a Tag 'Environment' = 'Production'
    """
    if not tags: return False
    
    for tag in tags:
        # Check if Key is Environment AND Value is Production
        if tag['Key'] == 'Environment' and tag['Value'] == 'Production':
            return True
    return False

def hunt_zombies():
    # Use Resource (It's easier and cleaner for this task)
    ec2 = boto3.resource('ec2', region_name='ap-south-1')
    
    # Calculate Time: 24 hours ago (UTC)
    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=24)
    
    # Filter 1: Only look at "running" instances
    # We can use server-side filters for speed
    instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
    )

    print("🧟 Starting Zombie Hunt...")

    for instance in instances:
        # Check 1: Is it old enough?
        # instance.launch_time is already timezone-aware (UTC)
        if instance.launch_time >= cutoff_time:
            continue # Too young, skip it

        # Check 2: Is it Production? (CRITICAL SAFETY)
        if check_is_production(instance.tags):
            print(f"🛡️ Skipping Production Instance: {instance.id}")
            continue

        # If we got here, it's a Zombie
        try:
            print(f"🧟 Found Zombie: {instance.id} (Owner: {instance.key_name})")
            
            # Action: Stop the instance
            instance.stop()
            logging.warning(f"⛔ STOPPED Zombie Instance: {instance.id}")
            
        except Exception as e:
            logging.error(f"Failed to stop {instance.id}: {e}")

if __name__ == "__main__":
    hunt_zombies()