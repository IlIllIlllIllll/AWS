#!/bin/bash
nohup docker run -p 8080:8080 $ACCOUNT_ID.dkr.ecr.ap-northeast-2.amazonaws.com/gateway:latest &