#!/bin/bash
# Create destination directory
mkdir -p /app/student-performance

# Install Docker correctly for Ubuntu 24
apt-get update -y
apt-get install -y docker.io

# Start docker
systemctl start docker
systemctl enable docker

# Install AWS CLI correctly
apt-get install -y unzip curl
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip -o awscliv2.zip
sudo ./aws/install --update