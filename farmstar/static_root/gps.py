import serial
import time
import os
import sys
import sqlite3
import datetime
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
    ser = None
    while True:
        try:
            if(ser == None or lines[0] == ''):
                ser = serial.Serial(comport,9600,timeout=1.5)
                print("Reconnecting")
            line = ser.readline().decode("utf-8") # Read the entire string
            lines = line.rstrip('\n\r').split(",")
            try:
                live = livePos(lines)
                print(live)
            except:
                print("Save Fail")
        except:
            if(not(ser == None)):
                ser.close()
                ser = None
                print("Disconnecting")
            print("No Connection")
            time.sleep(2)
        
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
def livePos(sentence):
        try:
            if sentence[0][3:] == 'GGA':
                lat = sentence[2]
                lon = sentence[4]
                x = lat[:2].lstrip('0') + "." + "%.7s" % str(float(lat[2:])*1.0/60.0).lstrip("0.")
                if sentence[3] == 'S':
                    xf = str('-'+x)
                else:
                    xf = str(x)
                y = lon[:3].lstrip('0') + "." + "%.7s" % str(float(lon[3:])*1.0/60.0).lstrip("0.")
                yf = str(y)            
                with open('live.geojson','w') as f:
                    f.write('{"geometry": {"type": "Point", "coordinates": [%s, %s]}, "type": "Feature", "properties": {}}' % (yf, xf))
                return(y,x)
            else:
                return("Invalid String")
        except:
            return("Save Fail")
            
serialStream()
