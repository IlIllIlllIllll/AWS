#!/bin/bash
ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.ap-northeast-2.amazonaws.com
docker pull $ACCOUNT_ID.dkr.ecr.ap-northeast-2.amazonaws.com/gateway:latest