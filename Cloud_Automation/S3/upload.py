import boto3

REGION = "ap-south-1"
BUCKET_NAME = "daksh-demo-bucket-for-python"
TXT_FILE = "./test_upload.txt"

client = boto3.client('s3', region_name="ap-south-1")

try:
    client.upload_file(TXT_FILE, BUCKET_NAME, "txt_files/test_upload.txt")
    print(f"{TXT_FILE} file uploaded to S3 successfully")
except FileNotFoundError as e:
    print(f"{TXT_FILE} not found")
except Exception as e:
    print("Error Occurred while uploading files", e)