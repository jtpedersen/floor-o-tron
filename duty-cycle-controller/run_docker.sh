#!/bin/bash 

set -x
set -e

# have export HA_TOKEN="long lived HA token" in env.sh file
source ../env.sh

docker build -t local/duty-cycle-controller:dev .


docker run --rm -it -p 5050:5050 \
       -e ha_token="${HA_TOKEN}" \
       -e DASH_URL="http://localhost:5050" \
       -v `pwd`/options.json:/data/options.json \
       local/duty-cycle-controller:dev 
