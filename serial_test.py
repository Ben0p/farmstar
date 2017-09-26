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
        return line
    
def create_raw_log():
    log_raw = 'serial_test.txt'
    if os.path.exists(log_raw)==False:
        print("No existing raw gps log file, attempting to create one...")
        try:
            open(log_raw,'w')
            open(log_raw,'w').close
        except IOError:
            print("Unable to create file")
        print("Raw GPS log file created OK!")
            
def open_raw_log():
    log_raw = 'serial_test.txt'
    try:
        raw_log = open(log_raw,"a")
    except:
        print("Computer syas no :(")
    return(raw_log)

def run():
    create_raw_log()
    while True:
        string = readString()
        raw_log = open_raw_log()
        print(string)
        raw_log.write(string)

run()
    
