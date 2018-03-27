#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import time
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))
from yocto_api import *
from yocto_power import *



#Idea: Make function to write to file and then have another fuction to
#draw out the graph as it is appended to the file by the sensor data.

def usage():
    scriptname = os.path.basename(sys.argv[0])
    print("Usage:")
    print(scriptname + ' <serial_number>')
    print(scriptname + ' <logical_name>')
    print(scriptname + ' any  ')
    sys.exit()


def die(msg):
    sys.exit(msg + ' (check USB cable)')

errmsg = YRefParam()

if len(sys.argv) < 2:
    usage()

target = sys.argv[1]



# Setup the API to use local USB devices
if YAPI.RegisterHub("usb", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

if target == 'any':
    # retreive any Power sensor
    sensor = YPower.FirstPower()
    if sensor is None:
        die('No module connected')
else:
    sensor = YPower.FindPower(target + '.power')

if not (sensor.isOnline()):
    die('device not connected')
#We're adding the loop here for outputting to the file.
counter = 0
while sensor.isOnline():
		write_data = open('wattageData.txt','a+')
		print("Power :  " + "%2.1f" % sensor.get_currentValue() + "W (Ctrl-C to stop)")
		write_data.write("%d,%2.1f \n" % (counter, sensor.get_currentValue()))
		write_data.close()
		YAPI.Sleep(1000)
		counter += 1
YAPI.FreeAPI()
