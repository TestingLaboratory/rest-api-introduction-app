#!/bin/sh
echo "Running $1 app on port $2"
nohup uvicorn "rest_introduction_app.$1:app" --host=0.0.0.0 --port="$2" > "$1.log" &
echo "Logging into file: $1.log"
echo "In progress"