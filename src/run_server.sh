#!/bin/bash

uvicorn app:app \
    --reload \
    --host=0.0.0.0 \
    --port=8000 \
    --ssl-keyfile=./key.pem \
    --ssl-certfile=./cert.pem
