## ECS
---
### create service
```shell
aws ecs create-service \
    --cluster <cluster name> \
    --task-definition <task-definition Name> \
    --enable-execute-command \
    --service-name <service Name> \
    --desired-count <count> \
    --network-configuration "awsvpcConfiguration={subnets=[<Subnet-id>,<Subnet-id],securityGroups=[sercurity-group-id],assignPublicIp=DISABLED or ENABLE}"
```