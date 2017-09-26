import time
import serial
import os

def open_comport():
    with open("config.txt") as f:
        for line in f:
            if "com" in line:
                port = line.split("= ",1)[1]
                cport = port.rstrip('\n\r')
                ser = serial.Serial(cport,9600,timeout=1) # Open Serial port
                open("config.txt").close
    return(ser)

def readString():
    ser = open_comport()
    while True:
        print(ser.read())
    
readString()
