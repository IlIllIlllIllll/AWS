## Elastic Load Balancer - Access Log
```
aws s3 mb s3://<S3 Bucket>
```

```
cat <<EOF>> s3-policy.json
{
  "Id": "Policy1692168064042",
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Stmt1692168062934",
      "Action": [
        "s3:PutObject"
      ],
      "Effect": "Allow",
      "Resource": "arn:aws:s3:::<S3 Bucket>/*",
      "Principal": {
        "AWS": [
          "<ELB-AccountID>"
        ]
      }
    }
  ]
}
EOF
```

```
aws s3api put-bucket-policy --bucket <S3 Bucket> --policy "file://s3-policy.json"
```

> ![ELB Access ID](https://github.com/IlIllIlllIllll/AWS/raw/main/ALB/img/image-1.png)