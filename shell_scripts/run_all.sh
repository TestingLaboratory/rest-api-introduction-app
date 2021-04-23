#!/bin/sh
## as it is not bash - but sh - it DOES NOT support arrays
## maybe some clever piping here?
nohup sh ./*/run_app.sh fundamentals 8080 \&
nohup sh ./*/run_app.sh token_auth 8081 \&
nohup sh ./*/run_app.sh challenge_primer 8082 \&
nohup sh ./*/run_app.sh reactor_challenge 8083 \&
nohup sh ./*/run_app.sh cryptocrypto_challenge 8084 \&
nohup sh ./*/run_app.sh genetics_challenge 8085 \&
nohup sh ./*/run_app.sh diatlov_pass_challenge 8086 \&
nohup sh ./*/run_app.sh collector_challenge 8087 \&
nohup sh ./*/run_app.sh catastrophy_challenge 8088 \&
python ./*/sleeper.py