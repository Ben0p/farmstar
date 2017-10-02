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

def stringGen():
    l = serialStreamList()
    t = time.time()
    l.insert(0,t)
    return(l)

def sql_log():
    global db
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
            print('Commit')


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

