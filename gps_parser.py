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

def reFormatString():
    global maxlist
    global sqlint
    timer = 0
    starttime = time.time()
    conn = sqlite3.connect(db)
    c = conn.cursor()
    while True:
        lines = stringGen()
        while lines:
            lines = stringGen()
            length = len(lines)
            table = lines[1]
            unix = time.time()
            for i in maxlist:
                if i[0] == lines[1]:
                    if i[1]+1 == length:
                        var_string = ', '.join('?' * length)
                        query_string = 'INSERT INTO %s VALUES (%s);' % (table, var_string)
                        c.execute(query_string ,lines)
                        print('=',lines)
                    elif i[1]+1 > length:
                        #print("greater, reformatting...")
                        diff = i[1]+1-length
                        #print("diff=", diff)
                        #sentence = line.rstrip('\n\r').split(",")
                        #print("Old:", sentence)
                        checksum = lines[-1]
                        #print("Checksum:", checksum.rstrip('\n\r'))
                        slicedstring = lines[:-1]
                        #print("Sliced: ", slicedstring)
                        extendedstring = []
                        extendedstring = slicedstring
                        for _ in range(diff):
                            extendedstring.append('')
                        #print("Extended:", extendedstring)
                        finalstring = []
                        finalstring = extendedstring
                        finalstring.append(checksum)
                        #print("New: ", finalstring)
                        length = len(finalstring)
                        var_string = ', '.join('?' * length)
                        query_string = 'INSERT INTO %s VALUES (%s);' % (table, var_string)
                        c.execute(query_string ,finalstring)                        
                        print('+',finalstring)
                    elif i[1]+1 < length:
                        print("less, script failure")
            timer = unix - starttime
            if timer >= sqlint:
                conn.commit()
                starttime = time.time()
                timer = 0
                print("commit")
    conn.commit()
    print("commit")
    print("End of file")

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

reFormatString()
#sql_log()
#run()

