# Solar Server

## setting up a Linux Apache MySQL PHP (LAMP) server on a Raspberry Pi
No need to setup the wordpress stuff, unless you plan on making a wordpress site.
https://projects.raspberrypi.org/en/projects/lamp-web-server-with-wordpress/9

After cloning this repo move the index.php file up one directory.

## getting solar data via the charge controller data power
See https://www.github.com/alexnathanson/EPSolar_Tracer

## getting server power consumption data via external Raspberry Pi + INA219
See https://learn.adafruit.com/adafruit-ina219-current-sensor-breakout/python-circuitpython for detailed wiring instructions and code


* Pi 3V3 to sensor Vcc
* Pi GND to sensor Gnd
* Pi SCL to sensor Scl
* Pi SDA to sensor Sda

Wire the USB- together and connect to GND of Pi
Connect the USB+ to the Vin+ and Vin- pins

Installing CircuitPython Libraries on Raspberry Pi
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi

If the power meter Pi and the server Pi are plugged in to the same circuit, they do not necessarily need to be connected by an additional ground wire.

Library API info: https://github.com/adafruit/Adafruit_CircuitPython_INA219/blob/master/adafruit_ina219.py

## Test Steps
### 1) initiate the server if its not already running
### 2) initiate the power meter
* must use python3 -> python3 [script name] [runtime in seconds]
* runtime should be at least 4X the test runtime + 2x60 seconds sleep time between test + 15 seconds at the beginning and end for good measure -> ((testruntime * 2) + 150)
### 3) immediately initiate the selenium test
* python [script name] [runtime in seconds]
* if runtime isn't specified, default runtime is 5 seconds
### 4) pscp the data from the power meter
### 5) bring data into jupyter notebook
