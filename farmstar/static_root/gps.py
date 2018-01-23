import serial
import time
import os
import sys
import sqlite3
from datetime import datetime
import config


db = config.db
maxlist = config.maxlist
sqlint = 10
comport = config.comport

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def serialStream():
    lines = ['']
    ser = None
    loopcount = 0
    starttime = time.time()
    try:
        conn = sqlite3.connect(db)
        c = conn.cursor()
    except:
        print("Failed to connect to database '%s'" % (db))
    while True:
        try:
            if(ser == None or lines[0] == ''):
                ser = serial.Serial(comport,9600,timeout=1.5)
                print("Reconnecting to %s" % (comport))
            line = ser.readline().decode("utf-8") # Read the entire string
            lines = line.rstrip('\n\r').split(",")
            try:
                nmeaParser(lines)
                #logDB(lines)
            except:
                print("Live position fail")
        except:
            if(not(ser == None)):
                ser.close()
                ser = None
                print("Disconnecting")
            print("No Connection to %s" % (comport))
            time.sleep(2)

def nmeaParser(sentence):
    try:
        try:
            if sentence[0][3:] == 'GGA':
                GGA = GGAParse(sentence)
                lat = GGA[0]
                lon = GGA[1]
                #tim = GGA[2]
            else:
                pass
        except:
            print("GGA parse error")
        #Print it all
        sys.stdout.flush()
        sys.stdout.write("Latitude: %s\nLongatude: %s   \r" % (lat,lon) )
        
        #print("Latitude: %s \nLongatude: %s\r" % (lat, lon))
    except:
        pass


def GGAParse(sentence):
    try:
        fix = sentence[1]
        lat = sentence[2]
        NS = sentence[3]
        lon = sentence[4]
        EW = sentence[5]
        qlty = sentence[6]
        sats = sentence[7]
        acc = sentence[8]
        alt = sentence[9]
        altu = sentence[10]
        geoidh = sentence[11]
        geoidu = sentence[12]
        age = sentence[13]
        dgpsid = sentence[14]
        #Time
        #t = datetime.strptime(fix, '%H%M%S')
        #tf = datetime.strftime(time)
        #Lattitude
        x = lat[:2].lstrip('0') + "." + "%.7s" % str(float(lat[2:])*1.0/60.0).lstrip("0.")
        if NS == 'S':
            xf = str('-'+x)
        else:
            xf = str(x)
        #Longatude
        y = lon[:3].lstrip('0') + "." + "%.7s" % str(float(lon[3:])*1.0/60.0).lstrip("0.")
        yf = str(y)
        return(xf,yf)
    except:
        return("GGA Error")

            
serialStream()
