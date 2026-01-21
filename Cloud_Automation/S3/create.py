import boto3

REGION = "ap-south-1"
BUCKET_NAME = "daksh-demo-bucket-for-python"

client = boto3.client('s3', region_name="ap-south-1")

try:
    if REGION == "us-east-1":
        # Don't accept CreateBucketConfiguration
        client.create_bucket(Bucket=BUCKET_NAME)
    else:
        client.create_bucket(Bucket=BUCKET_NAME, CreateBucketConfiguration={'LocationConstraint': REGION})
    print(f"Bucket Created Successfully -- ", BUCKET_NAME)
except Exception as e:
    print("Error Occurred while creating bucket:", e)