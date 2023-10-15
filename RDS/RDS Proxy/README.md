## RDS Proxy - Secrets Manager
---
**Create Secrets Manager on RDS Proxy**
```
aws secretsmanager create-secret
  --name "<Secrets Manager Name>"
  --description "Proxy SecretsManager"
  --region <Region>
  --secret-string '{"username":"<DB User Name>","password":"<DB Password>"}'
```

<br>

## Create IAM Policy on RDS PRoxy
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "secretsmanager:GetSecretValue",
            "Resource": [
                "<Secrets Manager Arn>"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "kms:Decrypt",
            "Resource": "arn:aws:kms:ap-northeast-2:account_id:key/<RDS KMS ID>",
            "Condition": {
                "StringEquals": {
                    "kms:ViaService": "secretsmanager.ap-northeast-2.amazonaws.com"
                }
            }
        }
    ]
}
```

```
aws iam create-policy --policy-name rds-proxy-policy --policy-document file://rds-proxy-policy.json
```

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": "rds.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

```
aws iam create-role --role-name rds-proxy --assume-role-policy-document file://rds-proxy-assume.json
```

```
aws iam attach-role-policy --role-name rds-proxy --policy-arn arn:aws:iam::<AccountID>:policy/rds-proxy-policy
```

<br>

**Create RDS Proxy**
```
https://cloudy-salary-132.notion.site/AWS-Aurora-RDS-RDS-Proxy-68a6c3fcbdab42aaa015798808f08d1d
```