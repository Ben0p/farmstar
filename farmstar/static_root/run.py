import serial
import time
import os
import sys
import sqlite3
import datetime

checklist = [[importConfig, "Configuration import"],
             ['getDB()', "Get database name"],
             ['DBfile', "Database file"],
             ['getComport', "Get comport"],
             ['testComport', "Testing comport"],
             ]


def run():
    for each_check in checklist:
        check_function = each_check[0]
        check_name = each_check[1]
        if check_function() == False:
            print("%s.....[Fail]" %(check_name))
        else:
            print("%s.....[OK]" %(check_name))
             

#Import Config
def importConfig():
    try:
        import config
    except:
        return(False)

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
        comport = config.comport
    except:
        return(False)

#Serial port connection
def testComport():
    return(False)

##    try:
##        if(ser == None or lines[0] == ''):
##            ser = serial.Serial(comport,9600,timeout=1.5)
##            print("Reconnecting to %s" % (comport))
##        line = ser.readline().decode("utf-8") # Read the entire string
##        lines = line.rstrip('\n\r').split(",")
##        try:
##            livePos(lines)
##            #logDB(lines)
##        except:
##            print("Live position fail")
##    except:
##        if(not(ser == None)):
##            ser.close()
##            ser = None
##            print("Disconnecting")
##        print("No Connection to %s" % (comport))
##        time.sleep(2)
    

'''
Do a pre-flight test in a linux boot style ...[OK]

1 - Check if there is a config file (then import)
    - else prompt to run setup
    
2 - Check for database and connect
    - else prompt to run setup

3 - Check serial port
    - loop a prompt "Connecting... (ctl+c to cancel)"

4 - Check time difference between GPS and device
    - Error on the time, automatically syncronize?

5 - Check GPS data and all the shit

6 - Whatever else?

99 - Once pre-flight completed, display static info [not scrolling]

'''

run()
