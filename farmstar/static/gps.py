import serial
import time
import os
import sys
import sqlite3
import datetime
import random
import pytz
import tzlocal
import config

comport = config.comport
ser = serial.Serial(comport,9600,timeout=1)
db = config.db
maxlist = config.maxlist
sqlint = 10

def serialStream():
    global ser
    while True:
        while ser.read().decode("utf-8") != '$': # Wait for the begging of the string
            pass # Do nothing
        line = ser.readline().decode("utf-8") # Read the entire string
        return(line)

def serialStreamList():
    lin = serialStream()
    line = lin.rstrip('\n\r')
    lines = line.split(",")
    return(lines)

def livePos():
    while True:
        sentence = serialStreamList()
        while sentence:
            sentence = serialStreamList()
            if sentence[0] == 'GPGGA':
                lat = sentence[2]
                lon = sentence[4]
                x = lat[:2].lstrip('0') + "." + "%.7s" % str(float(lat[2:])*1.0/60.0).lstrip("0.")
                xf = str('-'+x)
                xfs = float(xf)
                y = lon[:3].lstrip('0') + "." + "%.7s" % str(float(lon[3:])*1.0/60.0).lstrip("0.")
                yf = str(y)
                yfe = float(yf)
                with open('local_live.geojson','w') as f:
                    f.write('{"geometry": {"type": "Point", "coordinates": [%s, %s]}, "type": "Feature", "properties": {}}' % (yf, xf))
                    print(yf, xf)
                

livePos()

