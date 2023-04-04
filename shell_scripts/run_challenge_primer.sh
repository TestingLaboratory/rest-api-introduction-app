#!/bin/sh

nohup sh ./*/run_app.sh challenge_primer 8080 \&
python ./*/sleeper.py