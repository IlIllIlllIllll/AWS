## S3 - ETC

```python
import boto3

s3_client = boto3.client('s3')

def create_presigned_url(bucket_name, object_name, expiration):

    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3', aws_access_key_id='XXX', aws_secret_access_key='XXXX')
    response = s3_client.generate_presigned_url('get_object',
                                                Params={'Bucket': bucket_name,
                                                        'Key': object_name},
                                                ExpiresIn=expiration)

    return response

print(create_presigned_url('wsi-s3-pjm1024cl', 'index.png', '300'))
```