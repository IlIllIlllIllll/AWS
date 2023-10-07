## Install ECS-CLI
```shell
sudo curl -Lo /usr/local/bin/ecs-cli https://amazon-ecs-cli.s3.amazonaws.com/ecs-cli-linux-amd64-latest
sudo chmod +x /usr/local/bin/ecs-cli
```

### Environmental variables
```shell
export access=<root account key>
export secret=<root secret access key>
```

### Create IAM
```YAML
cat << EOF > task-execution-assume-role.json
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
EOF
```

``` shell
aws iam create-role --region ap-northeast-2 --role-name <Role Name> --assume-role-policy-document file://task-execution-assume-role.json
```

```shell
aws iam attach-role-policy -–region <region> --role-name <Role Name> --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

### Create cluster
```shell
ecs-cli up --cluster <Cluster Name> --empty
```

## stress
### Create stress config
```shell
ecs-cli configure --cluster <Cluster Name> --region ap-northeast-2 --default-launch-type FARGATE --config-name <stress config Name>
```

### Create stress profile
```shell
ecs-cli configure profile --access-key <access-key> --secret-key <secret-key> --profile-name <stress profile>
```

### docker-compose-stress.yaml
```yaml
version: '3' 
services:
  stress:
    image: <image>
    ports:
      - "<Port>:<Port>"
```

### ecs-params-stress.yaml
```yaml
version: 1
task_definition:
  task_execution_role: <Role Name>
  ecs_network_mode: awsvpc
  task_size:
    mem_limit: 0.5GB
    cpu_limit: 256
run_params:
  network_configuration: 
    awsvpc_configuration:
      subnets:
        - "<Subnet>" 
        - "<Subnet>"
      security_groups:
        - "<Security Group Id>"
      assign_public_ip: <ENABLED or DISABLED>
```

### Deploy stress ECS
```shell
ecs-cli compose --project-name <stress project Name> --file docker-compose-stress.yml --ecs-params ecs-params-stress.yml --debug service up --region <region> --cluster-config <stress config Name> --tags Name=<Name> --ecs-profile <stress profile> --target-groups "targetGroupArn=<target group Arn>,containerName=stress,containerPort=<Port>"
```

---
## product
### Create product config
```shell
ecs-cli configure --cluster <Cluster Name> --region <region> --default-launch-type FARGATE --config-name <config product name>
```

### Create product profile
```shell
ecs-cli configure profile --access-key <access-key> --secret-key <secret-key> --profile-name <product key>
```

### docker-compose-product.yaml
```yaml
version: '3' 
services:
  product:
    image: <image>
    ports:
      - "<Port>:<Port>"
```

### ecs-params-product.yaml
```yaml
version: 1
task_definition:
  task_execution_role: <Role Name>
  ecs_network_mode: awsvpc
  task_size:
    mem_limit: 0.5GB
    cpu_limit: 256
run_params:
  network_configuration: 
    awsvpc_configuration:
      subnets:
        - "<Subnet>" 
        - "<Subnet>"
      security_groups:
        - "<Security Group Id>"
      assign_public_ip: <ENABLED or DISABLED>
```

### Deploy product ECS
```shell
ecs-cli compose --project-name <product project Name> --file docker-compose-product.yml --ecs-params ecs-params.yml --debug service up --region <region> --cluster-config <product config Name> --tags Name=<Name> --ecs-profile <product profile Name> --target-groups "targetGroupArn=<target group Arn>,containerName=product,containerPort=<Port>"
```