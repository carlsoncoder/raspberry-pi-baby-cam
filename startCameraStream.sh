#!/bin/bash

if pgrep mjpg_streamer > /dev/null
then
  echo "mjpg_streamer already running"
else
  export LD_LIBRARY_PATH="/usr/local/lib"
  mjpg_streamer -i "input_raspicam.so -fps 20 -q 50 -x 1280 -y 720 -ex night" -o "output_http.so -p 9000 -w /usr/local/www" > /dev/null 2>&1&
  echo "mjpg_streamer started"
fi