## ECS CLI란?

Local Development Environment에서 Cluster Create, Updata, Monitoring을 간편하게 해주는 CLI

---
## Install ECS-CLI
```shell
sudo curl -Lo /usr/local/bin/ecs-cli https://amazon-ecs-cli.s3.amazonaws.com/ecs-cli-linux-amd64-latest
sudo chmod +x /usr/local/bin/ecs-cli
```

---
## Create Docker Image
(해당 Image는 Golang 기준으로 진행합니다.)

### Golang Application
```go
package main

import (
    "fmt"
    "net/http"
)

func health(w http.ResponseWriter, req *http.Request) {
    fmt.Fprint(w, "OK")
}

func main() {
    http.HandleFunc("/health", health)
    http.ListenAndServe(":8080", nil)
}
```


### Install Docker
```shell
sudo yum install -y docker
sudo systemctl enable --now docker
sudo usermod -aG docker ec2-user
sudo usermod -aG dockear root
sudo chmod 666 /var/run/docker.sock
```

### Create Dockerfile
```Docker
FROM golang:alpine
WORKDIR /app
COPY app.go .
RUN apk add --no-cache curl && go mod init noah.io/ark/rest && go build app.go
EXPOSE 8080
CMD ["./app"]
```

### Image Build
```shell
docker build -t app-ecr .
```

### Select Image
```shell
docker images
```
```shell
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
app-ecr      latest    14f663a34282   31 minutes ago   450MB
```

### Run Docker Container
```shell
docker run -d -p 8080:8080 app-ecr
```

### Status Check Docker Container
```shell
docker ps
```
```shell
CONTAINER ID   IMAGE      COMMAND    CREATED         STATUS        PORTS                                       NAMES
6abff0c5bcfa   app-ecr    "./app     3 seconds ago   Up 1 second   0.0.0.0:8080->8080/tcp, :::8080->8080/tcp   clever_boyd
```

### Upload ECR Repository
```shell
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account id>.dkr.ecr.ap-northeast-2.amazonaws.com

docker tag app-ecr:latest <account id>.dkr.ecr.ap-northeast-2.amazonaws.com/app-ecr:latest

docker push <account id>.dkr.ecr.ap-northeast-2.amazonaws.com/app-ecr:latest
```

## Create ECS on ECS-CLI
---

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

### Create config
```shell
ecs-cli configure --cluster <cluster> --region <region> --default-launch-type FARGATE --config-name <config Name>
```

### Create profile
```shell
ecs-cli configure profile --access-key $access --secret-key $secret --profile-name <profile Name>
```

## Create Compose File
---
### Create Docker-Compose
```yaml
version: '3'
services:
  <Container Name>:
    image: <image>
    ports:
      - "<port>:<port>"
```

### Create ECS-Params
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
      - "<subnet id>"
      - "<subnet id>"
      - "<subnet id>"
    security_groups:
      - "<security group id>"
    assign_public_ip: <ENABLED or DISABLED>
```
> assign_public_ip부분은 Public CIDR의 생성여부에 대분 부분입니다. 활성화시 ENABLED를 작성하고 비활성화시 DISABLED를 작성합니다.

## Deploy ECS
---
```shell
ecs-cli compose --project-name <project Name> --file docker-compose.yml --ecs-params ecs-params.yml --debug service up --region <region> --cluster-config <config Name> --tags Name=<Service Name> --ecs-profile <profile Name> --target-groups "targetGroupArn=<target group Arn>,containerName=<container Name>,containerPort=<Port>"
```

### delete cluster or service
---
```shell
ecs-cli compose --project-name <project Name> service down --cluster-config <config Name>

ecs-cli down --force --cluster-config <config Name>
```

### 주의 사항
> project Name은 task와 service이름으로 지정됩니다.