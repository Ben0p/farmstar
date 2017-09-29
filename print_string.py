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

ser = open_comport()

def readString():
    while True:
        while ser.read().decode("utf-8") != '$': # Wait for the begging of the string
            pass # Do nothing
        line = ser.readline().decode("utf-8") # Read the entire string
        return(line)
    
def splitLines():
    types = []
    x = 0
    print("Scanning for unique GPS sentances...")
    while x < 20:
        string = readString()
        line = string.rstrip('\n\r')
        lines = line.split(",")
        sentance = lines[0]
        types.append(sentance)
        unique = set(types)
        x += 1
    print(unique)
        

splitLines()
