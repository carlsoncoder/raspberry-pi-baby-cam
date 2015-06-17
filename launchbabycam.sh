#!/usr/bin/env bash

cd /
cd /home/pi/raspberry-pi-baby-cam/nodejswebsite
sleep 1
sudo forever start app.js

#sleep for 15 seconds to ensure NodeJS starts up properly
sleep 15

cd /home/pi/raspberry-pi-baby-cam
sudo python ./babycamrunner.py

cd /
