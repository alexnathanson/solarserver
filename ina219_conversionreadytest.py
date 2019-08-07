#test to determine maximum sample rate of ina219 via raspberry pi

import time
import board
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
#import datetime

i2c_bus = board.I2C()

ina219 = INA219(i2c_bus)

print("ina219 test")

# optional : change configuration to use 32 samples averaging for both bus voltage and shunt voltage
ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_128S
ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_128S
# optional : change voltage range to 16V
ina219.bus_voltage_range = BusVoltageRange.RANGE_16V


# display some of the advanced field
# see https://github.com/adafruit/Adafruit_CircuitPython_INA219/blob/master/adafruit_ina219.py class ADCResolution for details
print("Config register:")
print("  bus_voltage_range:    0x%1X" % ina219.bus_voltage_range)
print("  gain:                 0x%1X" % ina219.gain)
print("  bus_adc_resolution:   0x%1X" % ina219.bus_adc_resolution)
print("  shunt_adc_resolution: 0x%1X" % ina219.shunt_adc_resolution)
print("  mode:                 0x%1X" % ina219.mode)
print("  conversion ready bit: 0x%1X" % ina219.conversion_ready)
print("")

cCumulativeTests = []
vCumulativeTests = []

testTime = 10.0 #seconds per test

#clear sample lists
cSampleList = []
vSampleList = []

elapsedTime = time.time()
startTime = time.time()

#run each test for X seconds
while elapsedTime - startTime < testTime :
	if ina219.conversion_ready == 1:
		print("conversion ready bit: 0x%1X" % ina219.conversion_ready)

		bus_voltage = ina219.bus_voltage        # voltage on V- (load side)
	    #shunt_voltage = ina219.shunt_voltage    # voltage between V+ and V- across the shunt
	    current = ina219.current                # current in mA

	    cSampleList.append(current)
	    vSampleList.append(bus_voltage)
	else:
		print("  conversion ready bit: 0x%1X" % ina219.conversion_ready)
    
    elapsedTime = time.time()

#divide the amount of samples by 10 seconds to get the per second amount
cCumulativeTests.append(len(cSampleList)/10.0)
vCumulativeTests.append(len(vSampleList)/10.0)

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
