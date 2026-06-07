#!/bin/bash
# Login to ECR
aws ecr get-login-password --region us-east-2 | \
docker login --username AWS --password-stdin \
628270103657.dkr.ecr.us-east-2.amazonaws.com

# Pull latest image
docker pull 628270103657.dkr.ecr.us-east-2.amazonaws.com/student-performance-app:latest

# Stop existing container if running
docker stop student-app || true
docker rm student-app || true

# Run new container
docker run -d \
  --name student-app \
  -p 5000:5000 \
  -v /var/log/flask-app.log:/var/log/flask-app.log \
  628270103657.dkr.ecr.us-east-2.amazonaws.com/student-performance-app:latest
  