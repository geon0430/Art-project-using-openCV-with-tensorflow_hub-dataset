FROM python:3.8.10

RUN apt-get update && \
    apt-get install -y vim libgl1-mesa-glx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install numpy==1.22 opencv-python==4.5.3.56 jupyter tensorflow==2.12.0 tensorflow-hub Pillow