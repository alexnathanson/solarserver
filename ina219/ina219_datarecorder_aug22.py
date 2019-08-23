#test to determine maximum sample rate of ina219 via raspberry pi

import time
import sys
import board
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219, Mode
import datetime
import numpy as np
import pandas as pd
import csv

fileName = 'data/ina219-'+str(datetime.date.today())+'-'+str(int(time.time()))+'.csv' 

i2c_bus = board.I2C()

ina219 = INA219(i2c_bus)

print("ina219 test")

# optional : change configuration to use 32 samples averaging for both bus voltage and shunt voltage
ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_128S
ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_128S
# optional : change voltage range to 16V
ina219.bus_voltage_range = BusVoltageRange.RANGE_16V


ina219.mode = Mode.SVOLT_CONTINUOUS

# display some of the advanced field
# see https://github.com/adafruit/Adafruit_CircuitPython_INA219/blob/master/adafruit_ina219.py class ADCResolution for details
print("Arguments: " + str(sys.argv))
print("Config register:")
print("  bus_voltage_range:    0x%1X" % ina219.bus_voltage_range)
print("  gain:                 0x%1X" % ina219.gain)
print("  bus_adc_resolution:   0x%1X" % ina219.bus_adc_resolution)
print("  shunt_adc_resolution: 0x%1X" % ina219.shunt_adc_resolution)
print("  mode:                 0x%1X" % ina219.mode)
print("  conversion ready bit: 0x%1X" % ina219.conversion_ready)
print("")

dataDF = pd.DataFrame(columns=['mA','V','time'])

testTime = float(sys.argv[1])

#clear sample lists
#testResults = []

elapsedTime = time.time()
startTime = time.time()

print ("Starting!")
#run each test for X seconds
while elapsedTime - startTime < testTime :


	if ina219.conversion_ready == 1:

		bus_voltage = ina219.bus_voltage        # voltage on V- (load side)
	    #shunt_voltage = ina219.shunt_voltage    # voltage between V+ and V- across the shunt
		current = ina219.current                # current in mA
		
		dataDF = dataDF.append({'mA' : current , 'V' : bus_voltage, 'time': time.time()},ignore_index=True)

	#else:
		#print("  conversion ready bit: 0x%1X" % ina219.conversion_ready)

	elapsedTime = time.time()


print("Test time: {}".format(elapsedTime - startTime))
#divide the amount of samples by 10 seconds to get the per second amount
print("Samples per second: {}".format(len(dataDF)/testTime))
#print(testResults)

print(dataDF)

#save data to file
# check if the file already exists
try:
	with open(fileName) as csvfile:
		print("This file already exists!")
except:
	dataDF.to_csv(fileName, sep=',',index=False)