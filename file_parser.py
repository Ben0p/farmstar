import sqlite3
import time
import datetime
import serial
import sys
import platform
import os
import shutil
import socket
import tzlocal
import glob
from collections import defaultdict

config = 'fileconfig.py'
oldconfig = 'config.py.old'
gpsfile = 'serial_test.txt'
processedfile = 'serial_processed.txt'
timezone = tzlocal.get_localzone()
epocoffset = time.timezone
comportlist = []
comport = 'x'
sentencetypes = []
db = 'fileParser.db'
sentencelengths = []
openserial = 'x'
maxitems = []
maxlist = []
sqlint = 10


def timeNow():
    epoc = time.time()
    timenow = str(datetime.datetime.fromtimestamp(epoc).strftime('%d/%m/%Y %H:%M:%S'))
    return(epoc,timenow)

def fileParser():
    global sentencelengths
    global sentencetypes
    templist = []
    x = 0
    with open(gpsfile) as f:
        line = f.readline()
        while line and x <= 30:
            r = line.rstrip('\n\r')
            lines = r.split(",")
            segment = lines[0],len(lines)
            templist.append(segment)
            line = f.readline()
            x += 1
    f.close
    sentencelengths = set(templist)
    sentencelengths = [list(x) for x in sentencelengths]
    print(sentencelengths)
    templist = []
    for i in sentencelengths:
        templist.append(i[0])
    sentencetypes = set(templist)
    sentencetypes = list(sentencetypes)
    print(sentencetypes)

def groupItems():
    global sentencelengths
    global groupitems
    list_ = sentencelengths
    group = defaultdict(list)
    for vs in list_:
        group[vs[0]] += vs[1:]
    groupitems = group.items()
    groupitems = [list(x) for x in groupitems]
    print(groupitems)

def maxOnly():
    global groupitems
    global maxlist
    global maxitems
    global finallist
    templist = []
    for list_ in groupitems:
        for item in list_:
            for length in item:
                try:
                    templist.append(int(length))
                except ValueError:
                    pass
        maxlength = max(templist)
        maxitems = list_[0], maxlength
        maxlist.append(maxitems)
        templist = []
    maxlist = [list(x) for x in maxlist]
    print(maxlist)

def saveValues():
    global maxlist
    global groupitems
    global sentencetypes
    with open(config, 'a') as f:
        f.write("groupitems = %s\n" % groupitems)
        f.write("sentencetypes = %s\n" % sentencetypes)
        f.write("maxlist = %s\n" % maxlist)
        for i in maxlist:
            f.write("%smax = %s\n" %(i[0], i[1]))
        for i in groupitems:
            f.write("%s = %s\n" %(i[0], i[1]))

def createDatabase():
    global sentencetypes
    global db
    conn = sqlite3.connect(db)
    c = conn.cursor()
    print("Connected to '"+db+"' OK!")
    for i in sentencetypes:
        i.strip("'")
        print(i)
        c.execute("CREATE TABLE IF NOT EXISTS %s (unix INT)" % (i))
        conn.commit()
    with open(config,'a') as f:
        f.write("db = '%s'\n" % db)
        f.close
    print("Tables created OK!")

#This is some mozart script right here:
def populateTables():
    global db
    global maxlist
    conn = sqlite3.connect(db)
    c = conn.cursor()
    print("Populating tables...")
    for i in maxlist:
        sentence = i[0]
        length = i[1]   
        print("%s = %s" %(sentence, length))
        x = 1
        while x <= length:
            try:
                c.execute("ALTER TABLE %s ADD COLUMN '%s'" % (sentence, x))
                x += 1
            except:
                x += 1
                pass
    conn.commit()
    conn.close()
    print("Wow! Such script! Much columns!")

def reFormatString():
    global maxlist
    global sqlint
    timer = 0
    starttime = time.time()
    conn = sqlite3.connect(db)
    c = conn.cursor()
    with open(gpsfile) as f:
        line = f.readline()
        while line:
            r = line.rstrip('\n\r')
            lin = r.split(",")
            unix = time.time()
            lines = [unix]+lin
            length = len(lines)
            table = lines[1]
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
            line = f.readline()
    conn.commit()
    print("commit")
    print("End of file")
    
def run():
    timenow = timeNow()
    print(timenow[1])
    fileParser()
    groupItems()
    maxOnly()
    saveValues()
    createDatabase()
    populateTables()
    reFormatString()
        
run()
