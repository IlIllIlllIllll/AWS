## ECS
---
### ECS EXEC - Fargate
```shell
aws ecs run-task \
    --cluster <cluster Name>  \
    --task-definition <Taskdefinition Name> \
    --network-configuration awsvpcConfiguration="{subnets=[<Subnet ID>, subnet-00adfe3ed0c253049],securityGroups=[<Security-group-id],assignPublicIp=<DISABLED or ENABLED>}" \
    --enable-execute-command \
    --launch-type FARGATE \
    --tags key=environment,value=production \
    --platform-version '1.4.0' \
    --region <Region>
```

```shell
aws ecs execute-command  \
    --region <Region> \
    --cluster <cluster name> \
    --task <Taskdeinition arn> \
    --container <Container Name> \
    --command "</bin/bash or /bin/sh>" \
    --interactive
```

> Error
The Session Manager plugin was installed successfully. Use the AWS CLI to start a session.

An error occurred (InvalidParameterException) when calling the ExecuteCommand operation: The execute command failed because execute command was not enabled when the task was run or the execute command agent isn’t running. Wait and try again or run a new task with execute command enabled and try again. <br>
**Trouble-Shooting**
```shell
aws ecs update-service \
    --cluster <Cluster Name> \
    --service <Service Name> \
    --force-new-deployment
```