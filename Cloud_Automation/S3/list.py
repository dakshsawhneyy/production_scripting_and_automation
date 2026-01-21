import boto3

client = boto3.client('s3')
response = client.list_buckets()
buckets = response['Buckets']

for bucket in buckets:
    print(f"Name: {bucket['Name']} -- Creation Date: {bucket['CreationDate']}")