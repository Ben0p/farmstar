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

config = 'test123.py'
oldconfig = 'config.py.old'
gpsfile = 'serial_test.txt'
processedfile = 'serial_processed.txt'
timezone = tzlocal.get_localzone()
epocoffset = time.timezone
comportlist = []
comport = 'x'
sentencetypes = []
db = 'restringed'
sentencelengths = []
openserial = 'x'
maxitems = []


def timeNow():
    epoc = time.time()
    timenow = str(datetime.datetime.fromtimestamp(epoc).strftime('%d/%m/%Y %H:%M:%S'))
    return(epoc,timenow)

def fileParser():
    global sentencelengths
    lengths = []
    x = 0
    with open(gpsfile) as f:
        line = f.readline()
        while line and x <= 30:
            r = line.rstrip('\n\r')
            lines = r.split(",")
            segment = lines[0],len(lines)
            lengths.append(segment)            
            line = f.readline()
            x += 1
    sentencelengths = set(lengths)
    print(sentencelengths)
    
def getSentenceTypes():
    global config
    global sentencetypes
    with open(config) as f:
        for line in f:
            if "sentencetypes" in line:
                sentenc = line.split("= {",1)[1]
                sentence = sentenc.rstrip('}\n\r')
                sentencetypes = sentence.split(',')
                f.close

def sentenceLengths():
    lengths = []
    x = 0
    global sentencelengths
    while x < 20:
        lines = serialStreamList()
        segment = lines[0],len(lines)
        lengths.append(segment)
        unique = set(lengths)
        print
        x += 1
    sentencelengths = unique

def tupleToList():
    global sentencelengths
    a = sentencelengths
    sentencelengths = [list(x) for x in a]
    return(sentencelengths)

def groupItems():
    global sentencelengths
    global groupitems
    list_ = sentencelengths
    print(sentencelengths)
    group = defaultdict(list)
    for vs in list_:
        group[vs[0]] += vs[1:]
    groupitems = group.items()

def groupToList():
    global groupitems
    global maxlist
    a = groupitems
    maxlist = [list(x) for x in a]

def maxOnly():
    global groupitems
    global maxlist
    global maxitems
    global finallist
    templist = []
    newlist = []
    print(groupitems)
    print(maxlist)
    for list_ in maxlist:
        for item in list_:
            for length in item:
                try:
                    templist.append(int(length))
                    print(templist)
                except ValueError:
                    pass
        maxlength = max(templist)
        print("MAX: ", maxlength)
        maxitems = list_[0], maxlength
        print(maxitems)
        newlist.append(maxitems)
        templist = []
    finallist = newlist
    print(finallist)

def saveValues():
    global maxlist
    global finallist
    with open(config, 'a') as f:
        f.write("maxlist = %s\n" % maxlist)
        f.write("finallist = %s\n" % finallist)
        for i in maxlist:
            f.write(i[0] + "max = " + i[1], "\n")
        for i in finallist:
            f.write(i[0] + " = " + i[1] + "\n")

def reFormatString():
    global finallist
    with open(gpsfile) as f:
        line = f.readline()
        while line:
            r = line.rstrip('\n\r')
            lines = r.split(",")
            length = len(lines)
            for i in finallist:
                if i[0] == lines[0]:
                    if i[1] == length:
                        #print("same")
                        print(lines)
                    elif i[1] > length:
                        #print("greater, reformatting...")
                        diff = i[1]-length
                        #print("diff=", diff)
                        sentence = line.rstrip('\n\r').split(",")
                        #print("Old:", sentence)
                        checksum = sentence[-1]
                        #print("Checksum:", checksum.rstrip('\n\r'))
                        slicedstring = sentence[:-1]
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
                        print(finalstring)
                    elif i[1] < length:
                        print("less, script failure")
            line = f.readline()
        

def createDatabase():
    global sentencetypes
    global db
    global conn
    global c
    global config
    i = input("Do you wish to manually specify database name? (y/n)\n")
    while True:
        if i == 'y':
            d = input("Please enter desired database name exluding '.db'")
            db = d+'.db'
            if os.path.exists(db)==False:
                print("Database '"+db+"' not found, creating one now...")
                break
            else:
                print("Found existing database '"+db+"', connecting...")
                break
        elif i == 'n':
            d = platform.node()
            db = d+'.db'
            if os.path.exists(db)==False:
                print("Database '"+db+"' not found, creating one now...")
                break
            else:
                print("Database '"+db+"' exists, connecting...")
                break
    conn = sqlite3.connect(db)
    c = conn.cursor()
    print("Connected to '"+db+"' OK!")
    for i in sentencetypes:
        c.execute("CREATE TABLE IF NOT EXISTS %s (unix INT)" % (i))
        conn.commit()
    with open(config,'a') as f:
        f.write("db = '%s'" % db)
        f.close
    print("Tables created OK!")

#This is some mozart script right here:
def populateTables():
    global db
    global sentencelengths
    conn = sqlite3.connect(db)
    c = conn.cursor()
    print("Populating tables...")
    for i in sentencelengths:
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
    print("Wow! Such script! Much completion!")

        
    
def run():
    timenow = timeNow()
    print(timenow[1])
    fileParser()
    tupleToList()
    groupItems()
    groupToList()
    maxOnly()
    #saveValues()
    while True:
        print(reFormatString())
##    saveSentenceTypes()
##    getSentenceTypes()
##    print(sentencetypes)
##    sentenceLengths()
##    print(sentencelengths)
##    tupleToList()
##    merge_subs()
##    saveSentenceLengths()
##    saveNumberSentences()
##    createDatabase()
##    populateTables()
##    #raw_log()

run()
