#!/bin/bash

# docker build and docker run from args
# Usage: ./run.sh build/run
# Build the docker image

if [ "$1" == "build" ]; then
  docker build -t ml-predictor .
fi

# Run the docker container with environment variables
if [ "$1" == "run" ]; then
  docker run -v ${PWD}/.:/app -p 5000:5000 ml-predictor:latest
fi
