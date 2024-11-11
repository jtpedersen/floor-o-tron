#!/bin/bash 

set -x
set -e

source ../env.sh

docker build -t local/duty-cycle-controller:dev .


docker run --rm -it -p 5050:5050 \
       -e HA_URL="http://192.168.1.215:8123" \
       -e HA_TOKEN="${HA_TOKEN}" \
       -e DASH_URL="http://localhost:5050" \
       -v `pwd`/options.json:/data/options.json \
       local/duty-cycle-controller:dev 
