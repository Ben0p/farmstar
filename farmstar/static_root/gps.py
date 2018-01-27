import serial
import time
import os
import sys
import sqlite3
from datetime import datetime
import config
import curses


db = config.db
maxlist = config.maxlist
sqlint = 10
comport = config.comport
stdscr = curses.initscr()

#Initialize curses screen


def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def serialStream():
    lines = ['']
    ser = None
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
                #print(lines)
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

def screen(lat,NS,lon,EW,fix,age, sentence):
        stdscr = curses.initscr()
        stdscr.clear()
        stdscr.addstr(1,1," Latitude: %s %s" % (lat, NS))
        stdscr.addstr(2,1,"Longatude: %s %s" % (lon, EW))
        stdscr.addstr(3,1," GPS Time: %s" % (fix))
        stdscr.addstr(4,1,"      Age: %s" % (age))
        stdscr.addstr(5,1," Sentence: %s" % (sentence))
        stdscr.refresh()


def nmeaParser(sentence):
    
    try:
        try:
            if sentence[0][3:] == 'GGA':
                GGA = GGAParse(sentence)
                lat = GGA[0]
                NS = GGA[1]
                lon = GGA[2]
                EW = GGA[3]
                fix = GGA[4]
                age = GGA[5]
            else:
                pass
        except:
            print("GGA parse error")
        #screen(lat,NS,lon,EW,fix,age, sentence)
        #print(lat,NS,lon,EW)

        stdscr.clear()
        stdscr.addstr(5,1," Sentence: %s" % (sentence))
        stdscr.refresh()
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
        #Fix Time
        #t = datetime.strptime(fix, '%H%M%S')
        #ft = datetime.strftime(time)
        #Lattitude
        x = lat[:2].lstrip('0') + "." + "%.7s" % str(float(lat[2:])*1.0/60.0).lstrip("0.")
        if NS == 'S':
            xf = str('-'+x)
        else:
            xf = str(x)
        #Longatude
        y = lon[:3].lstrip('0') + "." + "%.7s" % str(float(lon[3:])*1.0/60.0).lstrip("0.")
        yf = str(y)
        return(xf,NS,yf,EW,fix, age)
    except:
        return("GGA Error")
            
serialStream()
