#!/bin/bash
# Create destination directory if it doesn't exist
mkdir -p /app/student-performance

# Install required packages
apt-get update -y
apt-get install -y docker.io awscli

# Start docker
systemctl start docker
systemctl enable docker