#!/bin/bash
set -e

sudo yum update -y
sudo yum install -y docker unzip
curl -fsSL https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -o /tmp/awscliv2.zip
unzip -q /tmp/awscliv2.zip -d /tmp
sudo /tmp/aws/install --update
sudo service docker start
sudo usermod -aG docker ec2-user
