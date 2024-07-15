#!/bin/bash

apt-get update

# install tools
apt-get install -y \
	git curl unzip vim wget yasm tmux 

apt-get install -y \
			libatlas-base-dev \
			libavcodec-dev \
			libavformat-dev \
			libavresample-dev \
			libboost-all-dev \
			libc6 \
			libc6-dev \
			libdc1394-22-dev \
			libcurl4- \
			libeigen3-dev \
			libexpat1-dev \
			libgl1-mesa-dri \
			libglew-dev \
			libnuma1 \
			libnuma-dev \
			libgtk-3-dev \
			libgtk2.0-dev \
			libgtkgl2.0-dev \
			libjpeg-dev \
			libjpeg-turbo8-dev \
			libopenexr-dev \
			libpng-dev \
			libpostproc-dev \
			libpq-dev \
			libqt5opengl5-dev \
			libsm6 \
			libswscale-dev \
			libtbb-dev \
			libtbb2 \
			libtiff-dev \
			libtiff5-dev \
			libtool \
			libv4l-dev \
			libwebp-dev \
			libx264-dev \
			libxext6 \
			libxine2-dev \
			libxrender1 \
			libxvidcore-dev \

rm /opt/hpcx/ompi/lib/libmpi.so.40
apt-get update
apt-get install -y libgl1-mesa-glx


