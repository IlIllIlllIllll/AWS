## Lambda Configuration
- link https://ap-northeast-2.console.aws.amazon.com/lambda/home?region=ap-northeast-2#/create/function

1. Generates a function.
    ```bash
    aws lambda create-function  --function-name dev-function   --runtime python3.10 --role arn:aws:iam::123456789999:role/service-role/lambda-role --zip-file fileb://lambda_function.zip --handler lambda_function.lambda_handler
    ```

2. lambda_function.zip content
   - lambda_function.py
    ```py
    import json

    def lambda_handler(event, context):
        # TODO implement
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }
    ```

3. 버전 생성
    ```cli
    aws lambda publish-version --function-name dev-function
    ```
3. lambda_alias
    ```bash
    aws lambda create-alias --function-name dev-function --function-version 1 --name development
    ```

- appspec.yaml
    ```bash
    version: 0.0
    Resources:
      - dev-function:
          Type: AWS::Lambda::Function
          Properties:
            Name: "dev-function"
            Alias: "development"
            CurrentVersion: 1
            TargetVersion: 2
    ```


- buildspec.yml

    ```bash
    version: 0.2

    phases:
      install:
        commands:
          - yum install -y zip
      pre_build:
        commands:
          - export CURRENT_VERSION=$(aws lambda get-alias --function-name dev-function --name development --query 'FunctionVersion' --output text)
          - NEW_VERSION=$((CURRENT_VERSION + 1))
          - export NEW_VERSION
          - zip lambda_function.zip lambda_function.py
      build:
        commands:
          - aws lambda create-alias --function-name dev-function --function-version $NEW_VERSION --name development
          - aws lambda update-function-code --function-name dev-function --zip-file fileb://lambda_function.zip
      post_build:
        commands:
          - sed -i "s/1/$CURRENT_VERSION/g" appspec.yaml
          - sed -i "s/2/$NEW_VERSION/g" appspec.yaml

    artifacts:
      files:
        - appspec.yaml
      discard-paths: yes
    cache:
      paths:
        - '/root/.m2/**/*'
    ```
- lambda_function.py
    ```py
    import json
    
    def lambda_handler(event, context):
        # TODO implement
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from test!')
        }
    ```