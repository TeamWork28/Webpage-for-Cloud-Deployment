#!/bin/bash

# Create destination directory if it doesn't exist
mkdir -p /app/student-performance

# Fix potential package manager locks
dpkg --configure -a

# Install required packages
apt-get update -y
apt-get install -y docker.io awscli

# Start Docker
systemctl start docker
systemctl enable docker