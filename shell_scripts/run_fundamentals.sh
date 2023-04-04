#!/bin/sh

nohup sh ./*/run_app.sh reactor_challenge 8080 \&
python ./*/sleeper.py