## IAM
---
### User

#### Create IAM User
```shell
aws iam create-user --user-name <User Name>
```

#### Create Access key on IAM User
```shell
aws iam create-access-key --user-name <User Name>
```
<br>

---
### Role

#### Create IAM Role
```shell
aws iam create-role --role-name <Role Name>
```
### Create IAM Assume Role
```shell
aws iam create-role --role-name <Role Name> --assume-role-policy-document file://<Assume Policy Path>
```

#### Create Auume Role Token
```shell
aws sts assume-role --role-arn <Role ARN> --role-session-name <Role Session Name>
```
> Assume Role Token을 발급하면 SessionToken이 생기는데 해당 SessionToken은 ~/.aws/credentials경로에 aws_security_token = "SessionToken" 의 형태로 붙여 넣어줘야 합니다.

<br>

---
### Policy

#### Create IAM Policy
```shell
aws iam create-policy --policy-name <Policy Name> --policy-document file://<Policy Path>
```

### Attach IAM Policy on IAM Role
```shell
aws iam attach-role-policy --role-name <Role Name> --policy-arn <Policy ARN>
```