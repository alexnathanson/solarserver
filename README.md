# Solar Server

## setting up a Linux Apache MySQL PHP (LAMP) server on a Raspberry Pi
sudo apt-get install apache2 -y<br>
sudo apt-get install php -y<br>
No need to setup the wordpress stuff, unless you plan on making a wordpress site.
https://projects.raspberrypi.org/en/projects/lamp-web-server-with-wordpress/9

To run tests, move the dropdown directory into /var/www/html<br>
To run the data collection web page move the index.php file into /var/www/html

## getting solar data via the charge controller data power
See https://www.github.com/alexnathanson/EPSolar_Tracer

## getting server power consumption data via external Raspberry Pi + INA219
See https://learn.adafruit.com/adafruit-ina219-current-sensor-breakout/python-circuitpython for detailed wiring instructions and code

* Pi 3V3 to sensor Vcc
* Pi GND to sensor Gnd
* Pi SCL to sensor Scl
* Pi SDA to sensor Sda

Preparing the USB cable
* cut a USB cable in half
* Solder the USB- wires of both halfs back together and connect to GND of Pi<br>
* Connect the USB+ of the incoming side to the Vin+ pin of the INA219
* Connect the USB+ of the outgoing side to the Vin- pin of the INA219

Installing CircuitPython Libraries on Raspberry Pi
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi

If the power meter Pi and the server Pi are plugged in to the same circuit, they do not necessarily need to be connected by an additional ground wire.

Library API info: https://github.com/adafruit/Adafruit_CircuitPython_INA219/blob/master/adafruit_ina219.py

## Running tests with Selenium 
https://selenium.dev/downloads/<br>
pip install pandas<br>
pip install selenium

## Test Steps
### 1) initiate the server if its not already running
### 2) initiate the power meter
* must use python3 -> python3 ina219_datarecorder_aug22.py [runtime in seconds]
* runtime should be at least 4X the test runtime + 2x60 seconds sleep time between test + 15 seconds at the beginning and end for good measure -> ((testruntime * 2) + 150)

### 3) immediately initiate the selenium test
* python selenium_imagesize_pingpong_aug24.py [runtime in seconds]
* if runtime isn't specified, default runtime is 5 seconds

### 4) pscp the data from the power meter to aggregator
pscp pi@POWER_METER_IP:solarserver/ina219/data/FILE_NAME c:\FULL_TEST_RESULTS_DIRECTORY_PATH

### 5) bring data into jupyter notebook
run aggregator_aug23.ipynb