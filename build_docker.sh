#!/bin/bash/

IMAGE_NAME="art-project-stylegan"

TAG="0.1"

docker build --no-cache -t ${IMAGE_NAME}:${TAG} .

