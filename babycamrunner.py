#!/usr/bin/env python

# Note - need to install the Adafruit LED Library here:
# https://github.com/adafruit/Adafruit_Python_LED_Backpack

# More info on this here:
# https://learn.adafruit.com/led-backpack-displays-on-raspberry-pi-and-beaglebone-black/

import os
import smbus
import RPi.GPIO as GPIO
from time import sleep
from Adafruit_LED_Backpack import Matrix8x8

buttonPin = 14
tempSensorAddress = 0x48
bus = smbus.SMBus(1)

videoActive = True
loopCounter = 0

display = Matrix8x8.Matrix8x8()
display.begin()
display.clear()
display.write_display()

GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN)

def write_display_letters():
    # displays the word "On" on the LED backpack
    display.set_pixel(2, 1, 1)
    display.set_pixel(3, 1, 1)
    display.set_pixel(4, 1, 1)

    display.set_pixel(5, 1, 1)
    display.set_pixel(5, 2, 1)
    display.set_pixel(5, 3, 1)

    display.set_pixel(2, 3, 1)
    display.set_pixel(3, 3, 1)
    display.set_pixel(4, 3, 1)

    display.set_pixel(2, 2, 1)

    display.set_pixel(2, 5, 1)
    display.set_pixel(3, 5, 1)
    display.set_pixel(4, 5, 1)
    display.set_pixel(4, 6, 1)
    display.set_pixel(4, 7, 1)
    display.set_pixel(3, 7, 1)
    display.set_pixel(2, 7, 1)

def enable_video_stream():
    print 'enabling video stream'
    os.system('sudo ./startCameraStream.sh')

    tempFile = open('./nodejswebsite/runningstatus.txt', 'wb')
    tempFile.write('1')
    tempFile.close()

    write_display_letters()
    display.write_display()

def disable_video_stream():
    print 'disabling video stream'
    os.system('sudo ./stopCameraStream.sh')

    tempFile = open('./nodejswebsite/runningstatus.txt', 'wb')
    tempFile.write('0')
    tempFile.close()

    display.clear()
    display.write_display()

def log_temperature():
    rvalue0 = bus.read_word_data(tempSensorAddress, 0)
    rvalue1 = (rvalue0 & 0xff00) >> 8
    rvalue2 = rvalue0 & 0x00ff
    rvalue = (((rvalue2 * 256) + rvalue1) >> 4) * 0.0625

    fahrenheit = rvalue * 1.8 + 32
    formatted = "{0:.1f}".format(fahrenheit)

    tempFile = open('./nodejswebsite/currenttemp.txt', 'wb')
    tempFile.write(formatted)
    tempFile.close()

    print 'the current temperature is ' + formatted

# always start the stream when the script starts
enable_video_stream()

while True:
    loopCounter += 1
    if loopCounter > 600:
        log_temperature()
        loopCounter = 0

    if GPIO.input(buttonPin) == False:
        # button was pressed - we need to act

        if videoActive:
            disable_video_stream()
            videoActive = False
        else:
            enable_video_stream()
            videoActive = True

        # sleep some extra time to prevent "extra" button presses
        sleep(0.5)

    sleep(0.1)