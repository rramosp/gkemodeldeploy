#!/bin/bash

# ------------ configure your settings -----------------

export ENDPOINT=http://35.223.222.112:8080
#export ENDPOINT=http://localhost:8080
export MODELSTR=gemma3-1b

export LOCUST_USERS=50
export LOCUST_RUN_TIME=200m   
export LOCUST_SPAWN_RATE=10

# ----------- do not edit below this line --------------

export LOCUST_LOCUSTFILE=src/locustfile.py
export LOCUST_HOST=$ENDPOINT
export LOCUST_AUTOSTART=true
export LOCUST_AUTOQUIT=5

locust 