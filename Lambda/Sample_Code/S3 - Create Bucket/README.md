## S3 - Create Bucket

```python
import boto3

s3 = boto3.client('s3')

bucket_name = '<S3 Bucket Name>'
file_key = '<Path>/<File Name>'
file_name = '/tmp/<File Name>'

def lambda_handler(event, context):
    s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstaraint': 'aws_region'})
```