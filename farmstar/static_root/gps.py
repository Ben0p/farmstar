import serial
import time
import os
import sys
import sqlite3
import datetime
import random
import pytz
import tzlocal
from . import config
from farmstar_gps.models import STATUS


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

def GPSstatus(status):
    p = STATUS(UNIX=time.time(), STATUS=status)
    p.save()
    obj = STATUS.objects.latest('id')
    s = obj.STATUS
    print(s)
    while s:
        livePos()
        obj = STATUS.objects.latest('id')
        s = obj.STATUS


def livePos():
    sentence = serialStreamList()
    if sentence[0] == 'GPGGA':
        lat = sentence[2]
        lon = sentence[4]
        x = lat[:2].lstrip('0') + "." + "%.7s" % str(float(lat[2:])*1.0/60.0).lstrip("0.")
        #xf = str('-'+x)
        y = lon[:3].lstrip('0') + "." + "%.7s" % str(float(lon[3:])*1.0/60.0).lstrip("0.")
        #yf = str(y)
        with open('live.geojson','w') as f:
            f.write('{"geometry": {"type": "Point", "coordinates": [%s, %s]}, "type": "Feature", "properties": {}}' % (y, x))
            

