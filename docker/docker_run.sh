#!/bin/bash

xhost +
docker run -it \
	--name geon_tensorflow_hub
       -p 41001:8888 \
       -p 40002:8080 \
        --network host \
	-e DISPLAY=$DISPLAY \
	--runtime nvidia \
	--gpus all \
	--restart always \
	-v /tmp/.X11-unix/:/tmp/.X11-unix \
	-v /home/geon/ \
	tensorflow_hub_gan:latest
