#!/bin/bash

# ------------ configure your settings -----------------

export ENDPOINT=http://localhost:8080
export MODELSTR=gemma3-1b
export HEADERHOST=35.226.252.191
export LOCUST_USERS=10
export LOCUST_RUN_TIME=5m
export LOCUST_SPAWN_RATE=50

# ----------- do not edit below this line --------------

export LOCUST_LOCUSTFILE=src/locustfile.py
export LOCUST_HOST=$ENDPOINT
export LOCUST_AUTOSTART=true
export LOCUST_AUTOQUIT=5

locust 