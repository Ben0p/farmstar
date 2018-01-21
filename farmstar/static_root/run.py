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

#Test the GPS data stream using the checksum value
def serialTest():
    try:
        print("Validating GPS data.....")
        ser = serial.Serial(comport,9600,timeout=1.5) #open serial port
        for _ in range(5): #read 5 lines only
            line = ser.readline().decode("utf-8") #read serial line 
            sentence = line.rstrip('\n\r') #remove the newline
            data = sentence[1:-3] #Gets 2nd to 4th last character in sentence to get nmea data
            checksum = sentence[-2:] #Gets last 2 characters (checksum)
            data_check = 0 #Start the xor operation at 0
            for c in data: #For each character in the nmea sentence
                data_check ^= ord(c) #Does a xor operation between previous character and current character
            hex_checksum = '0x'+checksum.lower() #adds '0x' to the front of the device checksum
            hex_data = format(data_check, '#04x')#converts to hex)
            if hex_data == hex_checksum:
                print("%s = %s.....[OK]" % (hex_checksum, hex_data))
            else:
                print("%s != %s.....[Fail]" % (hex_checksum, hex_data))
                return(False)        
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
