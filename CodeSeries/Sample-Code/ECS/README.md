## ECS bule green

1. taskdef.json Deploying Randomly
    ```
    {
        "executionRoleArn": "arn:aws:iam::123456789101:role/ecsTaskExecutionRole",
        "containerDefinitions": [
            {
                "name": "sample-website",
                "image": "nginx",
                "essential": true,
                "portMappings": [
                    {
                        "hostPort": 0,
                        "protocol": "tcp",
                        "containerPort": 80
                    }
                ]
            }
        ],
        "requiresCompatibilities": [
            "EC2"
        ],
        "networkMode": "bridge",
        "cpu": "512",
        "memory": "1024",
        "family": "skills-td"
    }
    ```

2. Create a task definition with taskdef.json
    ```bash
    aws ecs register-task-definition --cli-input-json file://taskdef.json
    ```
3. taskdef.json Rewriting
    ```json
    {
        "executionRoleArn": "arn:aws:iam::123456789101:role/ecsTaskExecutionRole",
        "containerDefinitions": [
            {
                "name": "sample-website",
                "image": "<IMAGE_URI>",
                "essential": true,
                "healthCheck": {
                    "retries": 3,
                    "command": [
                        "CMD-SHELL",
                        "curl -f http://localhost:80/ || exit 1"
                    ],
                    "timeout": 5,
                    "interval": 30,
                    "startPeriod": null
                },
                "portMappings": [
                    {
                        "hostPort": 0,
                        "protocol": "tcp",
                        "containerPort": 80
                    }
                ]
            }
        ],
        "requiresCompatibilities": [
            "EC2"
        ],
        "networkMode": "bridge",
        "cpu": "512",
        "memory": "1024",
        "family": "skills-td"
    }
    ```

4. Create DockerFile
    ```Dockerfile
    FROM golang:1.16.5
    RUN mkdir /app
    COPY main.go /app
    WORKDIR /app
    RUN go mod init example.com/m/v2 && go build -o main
    CMD ["./main"]
    ```

5. create ecr-repository
    ```bash
    aws ecr create-repository --repository-name skills-ecr
    ```

6. create buildspec.yaml
    ```yaml
    version: 0.2

    env:
      variables:
        AWS_ACCOUNT_ID: $(aws sts get-caller-identity --query 'Account' --output text) #Account ID Variable

    phases:
      install:
        commands:
      pre_build:
        commands:       # ecr login
          - aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.ap-northeast-2.amazonaws.com
          - DATA=$(date +"%Y-%m-%d.%H.%M.%S" -d "9 hours")  # tag value
      build:
        commands:   # build & push
          - docker build -t skills-ecr .
          - docker tag skills-ecr:latest $AWS_ACCOUNT_ID.dkr.ecr.ap-northeast-2.amazonaws.com/skills-ecr:$DATA
      post_build:
        commands:    # image definition
          - docker push $AWS_ACCOUNT_ID.dkr.ecr.ap-northeast-2.amazonaws.com/skills-ecr:$DATA
          - printf '{"ImageURI":"%s"}' $AWS_ACCOUNT_ID.dkr.ecr.ap-northeast-2.amazonaws.com/skills-ecr:$DATA > imageDetail.json
    artifacts:
      files:
        - taskdef.json
        - appspec.yaml
        - imageDetail.json
    ```

7. create appspec.yaml
    ```yaml
    version: 0.0
    Resources:
      - TargetService:
          Type: AWS::ECS::Service
          Properties:
            TaskDefinition: <TASK_DEFINITION>
            LoadBalancerInfo:
              ContainerName: "sample-website"
              ContainerPort: 80
    ```