#!/bin/sh

nohup sh ./*/run_app.sh reactor_challenge 8083 \&
python ./*/sleeper.py