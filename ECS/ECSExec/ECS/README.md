## ECS images
---
### Resolt

```shell
aws ecs run-task \
    --cluster <cluster Name>  \
    --task-definition <task definition Name> \
    --network-configuration awsvpcConfiguration="{subnets=[<Subnet ID>, subnet-00adfe3ed0c253049],securityGroups=[<Security-group-id],assignPublicIp=DISABLED or ENABLED}" \
    --enable-execute-command \
    --launch-type FARGATE \
    --tags key=environment,value=production \
    --platform-version '1.4.0' \
    --region <region>
```
task arn복사

```shell
aws ecs execute-command  \
    --region <region> \
    --cluster <cluster name> \
    --task <task arn> \
    --container <container Name> \
    --command "</bin/bash or /bin/sh>" \
    --interactive
```

### 만약 아래와 같은 error code가 떳을 시 대처 법
    The Session Manager plugin was installed successfully. Use the AWS CLI to start a session.

    An error occurred (InvalidParameterException) when calling the ExecuteCommand operation: The execute command failed because execute command was not enabled when the task was run or the execute command agent isn’t running. Wait and try again or run a new task with execute command enabled and try again.

<br>

```shell
aws ecs update-service \
    --cluster <cluster Name> \
    --service <service Name> \
    --force-new-deployment
```