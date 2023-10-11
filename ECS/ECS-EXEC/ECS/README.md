## ECS
---
### Create Infra on ECS
### Create cluster
```shell
aws ecs create-cluster --cluster-name <cluster Name> --tags key=Name,value=<cluster Name>
```

<br>

### Create Taskdefinition
![Select Launch Type Compatibility](https://github.com/IlIllIlllIllll/AWS/blob/main/ECS/ECS-EXEC/img/image-1.png)

![Create Taskdefinition](https://github.com/IlIllIlllIllll/AWS/blob/main/ECS/ECS-EXEC/img/image-2.png)

![Create Taskdefinition](https://github.com/IlIllIlllIllll/AWS/blob/main/ECS/ECS-EXEC/img/image-3.png)

![Create Taskdefinition](https://github.com/IlIllIlllIllll/AWS/blob/main/ECS/ECS-EXEC/img/image-4.png)

<br>

### Create Service
```shell
aws ecs create-service \
    --cluster <Cluster name> \
    --task-definition <task-definition Name> \
    --enable-execute-command \
    --service-name <Service Name> \
    --desired-count <Count> \
    --network-configuration "awsvpcConfiguration={subnets=[<Subnet-id>,<Subnet-id>],securityGroups=[<sercurity-group-id>],assignPublicIp=<DISABLED or ENABLE>}"