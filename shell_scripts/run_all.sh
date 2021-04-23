#!/bin/sh
nohup sh ./*/run_app.sh challenge_primer 8080 &
nohup sh ./*/run_app.sh reactor_challenge 8081 &
python ./*/sleeper.py