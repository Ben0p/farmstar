import serial
import time
import os
import sys
import sqlite3
import datetime
import random
import pytz
import tzlocal


def open_comport():
    with open("config.txt") as f:
        for line in f:
            if "com" in line:
                port = line.split("= ",1)[1]
                cport = port.rstrip('\n\r')
                ser = serial.Serial(cport,9600,timeout=1) # Open Serial port
                open("config.txt").close
    return(ser)

ser = open_comport()                

def readString():
    while True:
        while ser.read().decode("utf-8") != '$': # Wait for the begging of the string
            pass # Do nothing
        line = ser.readline().decode("utf-8") # Read the entire string
        return line

def db_name():
    with open("config.txt") as f:
        for line in f:
            if "db" in line:
                database = line.split("= ",1)[1]
                tb = hn.rstrip('\n\r')
                db = tb+'.db'
                open("config.txt").close
    return(db,tb)

def sql_init():
    database = db_name()
    db = database[0]
    tb = database[1]
    conn = sqlite3.connect(db)
    print("Databse "+db+" found OK!")
    c = conn.cursor()
    return(c)
    
def sql_log(lines):
    fix = getTime(lines[1], "%H%M%S", "%H:%M:%S")
    latlng = getLatLng(lines[2],lines[4])
    database = db_name()
    lat = latlng[0]
    lng = latlng[1]
    db = database[0]
    tb = database[1]
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("INSERT INTO "+tb+"(fix, lat, lng) VALUES (?, ?, ?)",
              (fix, lat, lng))
    conn.commit()
    

def getTime():
    epoc = time.time()
    zone = time.timezone
    timestring = datetime.datetime.fromtimestamp(epoc).strftime('%Y%m%d%H%M%S%f')
    return(timestring)

def timeZone():
    local_tz = tzlocal.get_localzone()
    return(local_tz)


def getLatLng(latString,lngString):
    latitude = latString[:2].lstrip('0') + "." + "%.7s" % str(float(latString[2:])*1.0/60.0).lstrip("0.")
    lng = lngString[:3].lstrip('0') + "." + "%.7s" % str(float(lngString[3:])*1.0/60.0).lstrip("0.")
    line = readString()
    lines = line.split(",")
    if lines[3] == 'S':
        lat = '-'+latitude
    else:
        lat = latitude
    return lat,lng


def log(lines):
    latlng = getLatLng(lines[2],lines[4])
    lat = latlng[0]
    lng = latlng[1]
    log = 'log.txt'
    if os.path.exists(log)==False:
        print("No existing gps log file, attempting to create one...")
        try:
            open(log,'w')
            open(log,'w').close
        except IOError:
            print("Unable to create log file")
        print("GPS log file created OK!")
    else:
        try:
            with open(log,"a") as f:
                f.write(lat + ',' + lng +'\n')
        except:
            print("nope?")
      

def splitLines():
    time = getTime()
    lin = readString()
    line = lin.rstrip('\n\r')
    lines = line.split(",")
    return(lines)

def stringGen():
    lines = splitLines()
    epoc = time.time()
    epocoffset = time.timezone
    string = [epoc] + [epocoffset] + lines
    return(string)

def run():
    while True:
        string = splitLines()
        time = getTime()
        if  string[1] == 'GPRMC':
            print(string)
            pass
        elif string[1] == 'GPGGA':
            print(string)
            pass

while True:
    print(stringGen())
#run()

