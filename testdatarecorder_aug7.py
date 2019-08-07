#test to determine maximum sample rate of ina219 via raspberry pi

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

cMeasurements = []
vMeasurements = []
timeStamps = []

totalElapsedTime = time.time()
testStartTime = time.time()

# length of test in seconds - needs to be started and run longer than the test runner is triggering data
# time stamp is used to sync of power data with server activity later
testTime = 5.0

print("Running test for {} seconds".format(testTime))

while totalElapsedTime - testStartTime < testTime :
 	
 	#clear sample lists
	cSampleList = []
	vSampleList = []

 	mElapsedTime = time.time()
 	mStartTime = time.time()

 	thisMeasurement = []
	#run each measurement for 1 seconds
	while mElapsedTime - mStartTime < 1.0 :
	    bus_voltage = ina219.bus_voltage        # voltage on V- (load side)
	    #shunt_voltage = ina219.shunt_voltage    # voltage between V+ and V- across the shunt
	    current = ina219.current                # current in mA

	    cSampleList.append(current)
	    vSampleList.append(bus_voltage)

	    mElapsedTime = time.time()

	#get the average current and voltage for the preceding second (could also use RMS)
	#if I'm just averaging - does it make a difference if I average here or do it all at the end?
	thisMeasurement.append(averageList(cSampleList))
	thisMeasurement.append(averageList(vSampleList))
	thisMeasurement.append(mStartTime)

totalElapsedTime = time.time() - startTime

print("Last second second: {}".format(thisMeasurement[len(thisMeasurement-1)]))

def averageList(listToAverage):

	myAvg = 0.0

	for a in listToAverage:
		myAvg+= a

	print("Samples collected in 1 second: {}".format(len(listToAverage)))

	return myAvg/len(listToAverage)

def rootMeanSquared(listToRMS):
	RMS = 0.0

	#some RMS equation

	return RMS