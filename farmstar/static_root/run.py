import serial
import time
import os
import sys
import sqlite3
import datetime

 

#Import Config
try:
    import config
except:
    print("Import config......[Fail]")
else:
    print("Import config......[OK]")

#Database name from config check
def getDB():
    try:
        global db
        db = config.db
    except:
        return(False)

#Database file check
def DBfile():
    if os.path.exists(db)==False:
        return(False)

#Serial Port config
def getComport():
    try:
        global comport
        comport = config.comport
    except:
        return(False)

#Serial port connection
def testComport():    
    try:
        ser = serial.Serial(comport,9600,timeout=1.5)
        ser.readline().decode("utf-8")
    except:
        return(False)

#Test the GPS data stream
def serialTest():
    try:
        ser = serial.Serial(comport,9600,timeout=1.5)
        for _ in range(5):
            line = ser.readline().decode("utf-8")
            sentence = line.rstrip('\n\r').split(",")
            #Do the checksum check or sum thing
            
    except:
        return(False)
    

#List of functions and description (checks)
checklist = [[getDB, "Get database name"],
             [DBfile, "Database file"],
             [getComport, "Get comport"],
             [testComport, "Testing comport"],
             [serialTest, "Validate gps data"],
             ]

# running through checks and printing result
def run():
    for each_check in checklist:
        check_function = each_check[0]
        check_name = each_check[1]
        if check_function() == False:
            print("%s.....[Fail]" %(check_name))
        else:
            print("%s.....[OK]" %(check_name))
            

run()
