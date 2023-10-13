#!/bin/bash
yum install docker -y
systemctl restart docker
usermod -aG docker ec2-user
chmod 666 /var/run/docker.sock