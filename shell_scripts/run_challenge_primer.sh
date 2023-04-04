#!/bin/sh

nohup sh ./*/run_app.sh challenge_primer 8081 \&
python ./*/sleeper.py