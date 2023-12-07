FROM python:3.8.10

    RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y vim libgl1-mesa-glx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install numpy==1.22 \
    pip install opencv-python==4.5.3.56 \ 
    pip intstall tensorflow==2.12.0 \
    pip install tensorflow-hub \
    pip inttall Pillo w\
    ln -s $(which python3) /usr/bin/python && \
    apt-get install -y libglib2.0-0 && \
    apt-get install -y libgl1-mesa-glx && \
    apt-get install -y vim && \
    apt-get install -y tmux && \
    apt-get install -y git && \
    pip install jupyter 

CMD ["bash"]
