# Solar Server

## setting up a Linux Apache MySQL PHP (LAMP) server on a Raspberry Pi
No need to setup the wordpress stuff, unless you plan on making a wordpress site.
https://projects.raspberrypi.org/en/projects/lamp-web-server-with-wordpress/9

After cloning this repo move the index.php file up one directory.

## getting solar data via the charge controller data power
See https://www.github.com/alexnathanson/EPSolar_Tracer

## getting server power consumption data via external Raspberry Pi + INA219
See https://learn.adafruit.com/adafruit-ina219-current-sensor-breakout/python-circuitpython for wiring instructions and code

Installing CircuitPython Libraries on Raspberry Pi
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi

If the power meter Pi and the server Pi are plugged in to the same circuit, they do not necessarily need to be connected by an additional ground wire.