import boto3

s3 = boto3.client('s3')

bucket_name = '<S3 Bucket Name>'
file_key = '<Path>/<File Name>'
file_name = '/tmp/<File Name>'

def lambda_handler(event, context):
    s3.download_file(bucket_name, file_key, file_name)