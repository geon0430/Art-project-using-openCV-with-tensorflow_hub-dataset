#!/bin/bash

port_num="1"
CONTAINER_NAME="geon_ArtMaker_StyleGan_Tensorflow"
IMAGE_NAME="art-project-stylegan"
TAG="0.1"

file_path=$(pwd)

docker run \
    --runtime nvidia \
    --gpus all \
    -it \
    -p ${port_num}2000:8000 \
    -p ${port_num}2888:8888 \
    --name ${CONTAINER_NAME} \
    --privileged \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ${file_path}:/ArtMaker_StyleGan_Tensorflow \
    --shm-size 5g \
    --restart=always \
    -w /ArtMaker_StyleGan_Tensorflow \
    -e DISPLAY=$DISPLAY \
    --device /dev/video0:/dev/video0 \
    ${IMAGE_NAME}:${TAG}
