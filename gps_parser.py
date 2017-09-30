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

def splitLines():
    lin = readString()
    line = lin.rstrip('\n\r')
    lines = line.split(",")
    return(lines)

def stringGen():
    l = splitLines()
    t = time.time()
    l.insert(0,t)
    return(l)

def db_name():
    with open("config.txt") as f:
        for line in f:
            if "db" in line:
                d = line.split("= ",1)[1]
                db = d.rstrip('\n\r')
                f.close
    return(db)

def sql_log():
    db = db_name()
    conn = sqlite3.connect(db)
    c = conn.cursor()
    x = 0
    while True:
        varlist = stringGen()
        table = varlist[1]
        var_string = ', '.join('?' * len(varlist))
        query_string = 'INSERT INTO %s VALUES (%s);' % (table, var_string)
        c.execute(query_string ,varlist)
        print('%s string written to db OK!' % table)
        x += 1
        if x == 10:
            conn.commit()
            x = 0
            print('commit')

#Not sure if we'll do this?
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

sql_log()
#run()

