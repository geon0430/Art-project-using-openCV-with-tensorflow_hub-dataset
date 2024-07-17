#!/bin/bash

# Adjust the key file path to the one without password
uvicorn app:app \
    --reload \
    --host=0.0.0.0 \
    --port=8000 \
    --ssl-keyfile=./inbic-rootca.key \
    --ssl-certfile=./inbic-rootca.crt
