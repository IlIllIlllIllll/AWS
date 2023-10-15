## RDS - IAM Authorization
---
### Create RDS DataBase

![Create RDS](https://github.com/IlIllIlllIllll/AWS/raw/main/RDS/RDS%20IAM%20Authorization/img/image-1.png)

![Create RDS](https://github.com/IlIllIlllIllll/AWS/raw/main/RDS/RDS%20IAM%20Authorization/img/image-2.png)

![Create RDS](https://github.com/IlIllIlllIllll/AWS/raw/main/RDS/RDS%20IAM%20Authorization/img/image-3.png)

![Create RDS](https://github.com/IlIllIlllIllll/AWS/raw/main/RDS/RDS%20IAM%20Authorization/img/image-4.png)

![Create RDS](https://github.com/IlIllIlllIllll/AWS/raw/main/RDS/RDS%20IAM%20Authorization/img/image-5.png)

![Create RDS](https://github.com/IlIllIlllIllll/AWS/raw/main/RDS/RDS%20IAM%20Authorization/img/image-6.png)

![Create RDS](https://github.com/IlIllIlllIllll/AWS/raw/main/RDS/RDS%20IAM%20Authorization/img/image-7.png)

![Create RDS](https://github.com/IlIllIlllIllll/AWS/raw/main/RDS/RDS%20IAM%20Authorization/img/image-8.png)


<br>

### Install Package
```
sudo dnf install -y mariadb105
```

```
sudo yum install -y wget
```

<br>

### Create SSL Certification
```
mkdir -p /var/mysql-certs
```

```
cd /var/mysql-certs
```

```
wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem
```

```shell
mysql -h <RDS MySQL Writer Endpoint> -P <Port> -u <User Name> -p
```

```sql
CREATE USER '<User Name>' IDENTIFIED WITH AWSAuthenticationPlugin AS 'RDS';
```

<br>

### Create Policy on RDS
```json
{
    "Version": "2012-10-17",
    "Statement": [
       {
          "Effect": "Allow", 
          "Action": [
              "rds-db:connect"
          ],
          "Resource": [
              "arn:aws:rds-db:<region>:<account ID>:dbuser:<RDS Resource ID>/<RDS User Name>"
 
          ]
 
       }
 
    ]
 
 }
```

```
aws iam create-policy --policy-name <policy Name> --policy-document file://<file path>
```

<br>

### Create Role on RDS
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sts:AssumeRole"
            ],
            "Principal": {
                "Service": [
                    "ec2.amazonaws.com"
                ]
            }
        }
    ]
}
```

```
aws iam create-role --role-name <Role Name> --assume-role-policy-document file://<file path>
```

```
aws iam attach-role-policy --role-name <Role> --policy-arn <Role arn>
```

```	
TOKEN="$(aws rds generate-db-auth-token --hostname <RDS MySQL Writer Endpoint> --port 3306 --region <Region> --username <User Name>)"
```

```shell
mysql -h <RDS MySQL Writer Endpoint> --ssl-ca=/var/mysql-certs/rds-combined-ca-bundle.pem --user=<User Name> --password=$TOKEN
```

> RDS - IAM Authorization - https://osmcloud.notion.site/RDS-IAM-ab92f84c5ce3486da73605436a727740?pvs=4