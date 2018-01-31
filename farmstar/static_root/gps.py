import serial
import time
import os
import sys
import sqlite3
from datetime import datetime
import config
import curses
from dateutil import tz


def serialStream():
    global comport
    global comstat
    global ser
    global line
    global db
    global dbstatus
    global conn
    global c
    global sentence
    comport = config.comport
    ser = None
    line = ''
    try:
        db = config.db
        conn = sqlite3.connect(db)
        c = conn.cursor()
        dbstatus = "[OK]"
    except:
        dbstatus = "[Fail]"
    while True:
        try:
            if(ser == None or line == ''):
                ser = serial.Serial(comport,9600,timeout=1.5)
                comstatus = "Reconnecting"
            line = ser.readline().decode("utf-8") # Read the entire string
            sentence = line.rstrip('\n\r').split(",")
            try:
                #print(line)
                run()
                #logDB(lines)
            except:
                print("Live position fail")
        except:
            if(not(ser == None)):
                ser.close()
                ser = None
                comstatus = "Disconnecting"
            print("No Connection to %s" % (comport))
            time.sleep(2)



def nmeaParser():
    global GGA_
    NMEA = sentence[0][3:]
    if NMEA == 'GGA':
        try:
            GGA_ = line
            GGAParse()
        except:
            pass
    else:
        pass

    
def GGAParse():
    global GGA_fix
    global GGA_lat
    global GGA_NS
    global GGA_lon
    global GGA_EW
    global GGA_qlty
    global GGA_sats
    global GGA_acc
    global GGA_alt
    global GGA_altu
    global GGA_geoidh
    global GGA_geoisu
    global GGA_age
    global GGA_dgpsid
    try:
        GGA_fix = sentence[1]
        GGA_lat = sentence[2]
        GGA_NS = sentence[3]
        GGA_lon = sentence[4]
        GGA_EW = sentence[5]
        GGA_qlty = sentence[6]
        GGA_sats = sentence[7]
        GGA_acc = sentence[8]
        GGA_alt = sentence[9]
        GGA_altu = sentence[10]
        GGA_geoidh = sentence[11]
        GGA_geoidu = sentence[12]
        GGA_age = sentence[13]
        GGA_dgpsid = sentence[14]

        #Lattitude
        x = GGA_lat[:2].lstrip('0') + "." + "%.7s" % str(float(lat[2:])*1.0/60.0).lstrip("0.")
        if GGA_NS == 'S':
            GGA_lat = str('-'+x)
        else:
            GGA_lat = str(x)
            
        #Longatude
        y = GGA_lon[:3].lstrip('0') + "." + "%.7s" % str(float(lon[3:])*1.0/60.0).lstrip("0.")
        GGA_lon = str(y)
        try:
            #Fix Time
            gpsTime(GGA_fix)
        except:
            GGA_fixutc = ""
            GGA_fixlocal = ""
    except:
        return("GGA Error")


def gpsTime(fix):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    fixtime = datetime.strptime(fix, '%H%M%S')
    GGA_fixutc = fixtime.strftime('%H:%M:%S')
    utc = datetime.utcnow()
    utcdate = utc.strftime('%Y-%m-%d')
    gpsutcdatetime = str("%s %s" % (utcdate, fixtimetime))
    fixutcdatetime = datetime.strptime(gpsutcdatetime, '%Y-%m-%d %H:%M:%S')
    gpsdatetime = fixutcdatetime.replace(tzinfo=from_zone)
    gpslocal = gpsdatetime.astimezone(to_zone)
    GGA_fixlocal = gpslocal.strftime('%H:%M:%S')

def screen():
        stdscr = curses.initscr()
        stdscr.clear()
        stdscr.addstr(1,1,"     GPGGA: %s" % (GGA_))
        stdscr.addstr(2,1,"  Latitude: %s %s" % (GGA_lat, GGA_NS))
        stdscr.addstr(3,1," Longatude: %s %s" % (GGA_lon, GGA_EW))
        stdscr.addstr(4,1,"  GPS Time: %s" % (GGA_fixutc))
        stdscr.addstr(5,1,"Local Time: %s" % (GGA_fixlocal))
        stdscr.addstr(6,1,"       Age: %s" % (GGA_age))
        stdscr.refresh()

def run():
    try:
        nmeaParser()
    except:
         print("NMEA Fail")
    try:
        screen()
    except:
        print("Screen Fail")


serialStream()
