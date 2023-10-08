## CloudFront - Invalidations

```python
import boto3

cfn = boto3.client('cloudfront')
cfn_id = "<CloudFront ID>"

def lambda_handler(event, context):
    res = cfn.create_invalidation(
        DistributionId=cfn_id,
        InvalidationBatch={
            'Paths': {
                'Quantity': 1,
                'Items': [
                    '/*',
                ]
            },
            'CallerReference': str(time.time()).replace(".", "")
        }
    )
    invalidation_id = res['Invalidation']['Id']
    return invalidation_id
```