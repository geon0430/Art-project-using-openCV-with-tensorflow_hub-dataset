FROM nvcr.io/nvidia/pytorch:23.01-py3

ENV TZ=Asia/Seoul
ENV DEBIAN_FRONTEND=noninteractive

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES all

COPY . /Art-project-using-openCV-tensorflow/

RUN apt-get update && \
    apt-get install -y python3 python3-pip

RUN if [ -e /usr/bin/python ]; then rm /usr/bin/python; fi && \
    ln -s $(which python3) /usr/bin/python

RUN bash /Art-project-using-openCV-tensorflow/setting-scripts/install_pip.sh
RUN bash /Art-project-using-openCV-tensorflow/setting-scripts/install_dependencies.sh
RUN bash /Art-project-using-openCV-tensorflow/setting-scripts/install_opencv.sh

RUN apt-get update


