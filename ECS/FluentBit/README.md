## FluentBit
---
### Install FluentBit on ECS
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": "ecs-tasks.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

<br>

```shell
aws iam create-role --role-name ecsTaskExecutionRole --assume-role-policy-document file://asumme-task.json
```

<br>

```shell
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy --role-naem ecsTaskExecutionRole
```

<br>

```shell
aws iam attach-role-policy --policy-arn arn:aws:iam::aws:policy/CloudWatchLogsFullAccess --role-name ecsTaskExecutionRole
```

<br>

![taskdefinition](https://github.com/IlIllIlllIllll/ECS/raw/main/FluentBit/img/image-1.png)

![taskdefinition Role](https://github.com/IlIllIlllIllll/ECS/raw/main/FluentBit/img/image-2.png)

![taskdefinition OS](https://github.com/IlIllIlllIllll/ECS/raw/main/FluentBit/img/image-3.png)

![taskdefinition Exection Role](https://github.com/IlIllIlllIllll/ECS/raw/main/FluentBit/img/image-4.png)

![taskdefinition Log Router](https://github.com/IlIllIlllIllll/ECS/raw/main/FluentBit/img/image-5.png)

![taskdefinition Log Router Container](https://github.com/IlIllIlllIllll/ECS/raw/main/FluentBit/img/image-6.png)

<br>

Log_router

![taskdefinition Log Container Setting](https://github.com/IlIllIlllIllll/ECS/raw/main/FluentBit/img/image-7.png)

<br>

App_container

![taskdefinition Container Setting](https://github.com/IlIllIlllIllll/ECS/raw/main/FluentBit/img/image-8.png)

![Logging Result](https://github.com/IlIllIlllIllll/ECS/raw/main/FluentBit/img/image-9.png)

![Logging Result](https://github.com/IlIllIlllIllll/ECS/raw/main/FluentBit/img/image-10.png)

> https://velog.io/@junhoskills10/ECS-TaskDefintion-FireLens-%ED%86%B5%ED%95%A9-%ED%99%9C%EC%84%B1%ED%99%94 <br>
https://github.com/aws-samples/amazon-ecs-firelens-examples