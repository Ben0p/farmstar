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
#from farmstar_gps.models import STATUS



db = config.db
maxlist = config.maxlist
sqlint = 10
comport = config.comport
#ser = serial.Serial(comport,9600,timeout=1)
#.isOpen() - checks if comport is open

def serialStream():
    lines = ['']
    while True:
        try:
            ser = serial.Serial(comport,9600,timeout=1)
            break
        except:
            print("No Connection")
            time.sleep(2)
    while True:
        try:
            if(ser == None or lines[0] == ''):
                ser = serial.Serial(comport,9600,timeout=1)
                print("Reconnecting")
            line = ser.readline().decode("utf-8") # Read the entire string
            lines = line.rstrip('\n\r').split(",")
            print(lines)
        except:
            if(not(ser == None)):
                ser.close()
                ser = None
                print("Disconnecting")
            print("No Connection")
            time.sleep(2)
        
    

##def serialStreamList():
##    while not serialStream():
##        lin = serialStream()
##        line = lin.rstrip('\n\r')
##        lines = line.split(",")
##        return(lines)
##    else:
##        return(False)
    

##def GPSstatus(status):
##    STATUS(UNIX=time.time(), STATUS=status).save() #Save True or False in STATUS table(django model)
##    #p.save()#Save True or False in STATUS table
##    s = STATUS.objects.latest('id').STATUS #Get latest status from table
##    print(s)
##    while s:
##        livePos()
##        obj = STATUS.objects.latest('id')
##        s = obj.STATUS

#Fix this:
def livePos():
    while serialStream() != False:
        sentence = serialStream()
        print(sentence)
        if sentence[0] == 'GPGGA':
            lat = sentence[2]
            lon = sentence[4]
            x = lat[:2].lstrip('0') + "." + "%.7s" % str(float(lat[2:])*1.0/60.0).lstrip("0.")
            #xf = str('-'+x)
            y = lon[:3].lstrip('0') + "." + "%.7s" % str(float(lon[3:])*1.0/60.0).lstrip("0.")
            #yf = str(y)
            with open('live.geojson','w') as f:
                f.write('{"geometry": {"type": "Point", "coordinates": [%s, %s]}, "type": "Feature", "properties": {}}' % (y, x))
            

while True:
    print(serialStream())
