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

# display some of the advanced field (just to test)
print("Config register:")
print("  bus_voltage_range:    0x%1X" % ina219.bus_voltage_range)
print("  gain:                 0x%1X" % ina219.gain)
print("  bus_adc_resolution:   0x%1X" % ina219.bus_adc_resolution)
print("  shunt_adc_resolution: 0x%1X" % ina219.shunt_adc_resolution)
print("  mode:                 0x%1X" % ina219.mode)
print("")

# optional : change configuration to use 32 samples averaging for both bus voltage and shunt voltage
ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
# optional : change voltage range to 16V
ina219.bus_voltage_range = BusVoltageRange.RANGE_16V

# measure and display loop

startTime = time.time()
elapsedTime = time.time()
cSampleList = []
vSampleList = []

while elapsedTime - startTime < 10.0 :
    bus_voltage = ina219.bus_voltage        # voltage on V- (load side)
    #shunt_voltage = ina219.shunt_voltage    # voltage between V+ and V- across the shunt
    current = ina219.current                # current in mA

    cSampleList.append(current)
    vSampleList.append(bus_voltage)
    # INA219 measure bus voltage on the load side. So PSU voltage = bus_voltage + shunt_voltage
    #print("PSU Voltage:   {:6.3f} V".format(bus_voltage + shunt_voltage))
    #print("Shunt Voltage: {:9.6f} V".format(shunt_voltage))
    #print("Load Voltage:  {:6.3f} V".format(bus_voltage))
    #print("Current:       {:9.6f} A".format(current/1000))
    #print("Power:       {:9.6f} A".format((current/1000) * bus_voltage))
    #print("")

    #time.sleep(2)

print("Current samples per second: {}".format(len(cSampleList)/10.0))
print("Voltage samples per second: {}".format(len(vSampleList)/10.0))