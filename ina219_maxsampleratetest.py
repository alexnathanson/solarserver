# from https://github.com/adafruit/Adafruit_CircuitPython_INA219
# wiring and installation instructions https://learn.adafruit.com/adafruit-ina219-current-sensor-breakout/python-circuitpython

'''
# some other test code
import board
import busio
import adafruit_ina219
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_ina219.INA219(i2c)

print("Bus Voltage:   {} V".format(ina219.bus_voltage))
print("Shunt Voltage: {} mV".format(ina219.shunt_voltage / 1000))
print("Current:       {} mA".format(ina219.current))
'''

"""Sample code and test for adafruit_in219"""

import time
import board
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
#import datetime

i2c_bus = board.I2C()

ina219 = INA219(i2c_bus)

print("ina219 test")

# optional : change configuration to use 32 samples averaging for both bus voltage and shunt voltage
ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
# optional : change voltage range to 16V
ina219.bus_voltage_range = BusVoltageRange.RANGE_16V

startTime = time.time()
elapsedTime = time.time()
cSampleList = []
vSampleList = []

cCumulativeTests = []
vCumulativeTests = []

testAmt = 10
#run the test X times
while testNum < testAmt:
	
	print("Test #{}".format(testNum))

	#run each test for 10 seconds
	while elapsedTime - startTime < 10.0 :
	    bus_voltage = ina219.bus_voltage        # voltage on V- (load side)
	    #shunt_voltage = ina219.shunt_voltage    # voltage between V+ and V- across the shunt
	    current = ina219.current                # current in mA

	    cSampleList.append(current)
	    vSampleList.append(bus_voltage)

	    elapsedTime = time.time()

	#divide the amount of samples by 10 seconds to get the per second amount
	cCumulativeTests.append(len(cSampleList)/10.0)
	vCumulativeTests.append(len(vSampleList)/10.0)

	testNum+=1

#get the average test sample amount
getAvgC = 0.0;
getAvgV = 0.0;

for x in cCumulativeTests:
	getAvgC += x

for x in vCumulativeTests:
	getAvgV += x

getAvgC = getAvgC/testAmt
getAvgV = getAvgV/testAmt

print("Current samples per second: {}".format(getAvgC))
print("Voltage samples per second: {}".format(getAvgV))
