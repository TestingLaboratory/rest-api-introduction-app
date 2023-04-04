#!/bin/sh

nohup sh ./*/run_app.sh fundamentals 8080 \&
python ./*/sleeper.py