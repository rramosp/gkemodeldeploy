#!/bin/bash

# ------------ configure your settings -----------------

export ENDPOINT=http://35.226.252.191:8000
export MODELSTR=gemma3-1b
export HEADERHOST=35.226.252.191
export LOCUST_USERS=200
export LOCUST_RUN_TIME=30s
export LOCUST_SPAWN_RATE=50

# ----------- do not edit below this line --------------

export LOCUST_LOCUSTFILE=src/locustfile.py
export LOCUST_HOST=$ENDPOINT
export LOCUST_AUTOSTART=true
export LOCUST_AUTOQUIT=5

locust 