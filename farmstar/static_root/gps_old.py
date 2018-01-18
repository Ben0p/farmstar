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

'''
This is more art than practical
WTF does this even do?
1. Reads GPS string
2. Compares length of each string in list form to the maximum length observed in the setup generated config.py
3. If the length is the same: record each value into the relevent table and columns
4. Else: remove the checksum from the end, extend the list to match the maxlength, attatch the checksum to the end.
(This is completely pointless because that invalids the checksum lolwutwhy)
(the whole point of this is because you have to insert an entire row into the database, not partial rows, atleast as far as I can google.)
5. Commits at every (sqlint) seconds (10)


'''
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
            lines = stringGen() # There is a reason this is here twice, can't remember why
            length = len(lines)
            table = lines[1]
            unix = time.time()
            for i in maxlist:
                if i[0] == lines[1]:
                    if i[1]+1 == length:
                        var_string = ', '.join('?' * length)
                        query_string = 'INSERT INTO %s VALUES (%s);' % (table, var_string)
                        c.execute(query_string ,lines)
                        #print('=',lines)
                    elif i[1]+1 > length:
                        diff = i[1]+1-length
                        checksum = lines[-1]
                        slicedstring = lines[:-1]
                        extendedstring = []
                        extendedstring = slicedstring
                        for _ in range(diff):
                            extendedstring.append('')
                        finalstring = []
                        finalstring = extendedstring
                        finalstring.append(checksum)
                        length = len(finalstring)
                        var_string = ', '.join('?' * length)
                        query_string = 'INSERT INTO %s VALUES (%s);' % (table, var_string)
                        c.execute(query_string ,finalstring)                        
                        #print('+',finalstring)
                    elif i[1]+1 < length:
                        print("less, script failure :(")
            timer = unix - starttime
            if timer >= sqlint:
                conn.commit()
                starttime = time.time()
                timer = 0
                print("commit")
    conn.commit()
    print("commit")
    print("End of file")

reFormatString()


