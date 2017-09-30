import sqlite3
import time
import datetime
import random
import serial
import sys
import shutil
import glob
import pynmea
import pathlib
import platform
import os
import socket
import pytz
import tzlocal


def config_backup():
    print("This script will generate a config file 'config.txt'")
    print("If file exists, it will be moved to 'config.txt.old'")
    print("If 'config.txt.old' exists, it will be overwritten!")
    while True:
        c = input("Continue? (y/n):\n")
        if c == 'y':
            print("Lets do it!\n")
            break
        if c == 'n':
            print("Understandable, have a nice day!")
            time.sleep(3)
            sys.exit()
        else:
            print("Please press either 'y' or 'n'")
    running_config = 'config.txt'
    backup_config = 'config.txt.old'
    if os.path.exists(running_config)==False:
        print("No config file exists, attempting to create one...")
        try:
            open(running_config,'w')
            open(running_config,'w').close
        except IOError:
            print("Unable to create file")
        print("Blank config file created OK!")
    else:
        try:
            shutil.copyfile(running_config, backup_config)
            print("Existing config backed up.")
            open(running_config,'w')
            print("Config now blank.\n")
        except IOError:
            print("Unable to read file.")

def timeZone():
    local_tz = tzlocal.get_localzone()
    return(local_tz)

def epocOffset():
    epoc_offset = time.timezone
    return(epoc_offset)
                   
def current_time():
    unix_time = time.time()
    date_time = str(datetime.datetime.fromtimestamp(unix_time).strftime('%d/%m/%Y %H:%M:%S'))
    return date_time
    
def check_time():
    while True:
        time = current_time()
        timezone = timeZone()
        epocoffset = epocOffset()
        print(time)
        print(timezone)
        t = input("Is this the correct time and zone? (y/n):\n")
        if t == 'y':
            with open('config.txt','a') as running_config:
                running_config.write('created = %s\n'
                                     'timezone = %s\n'
                                     'epocoffset = %s\n'
                                     % (time, timezone, epocoffset))
            
            print("OK!\n")
            return
        if t == 'n':
            while True:
                c = input("Please set your machine to the correct time and press 'c':\n")
                if c == 'c':
                    break
                else:
                    print("Please press 'c' only.")
        else:
            print("Please press either 'y' or 'n'")
        
def check_system():
    arch = platform.machine()
    ver = platform.version()
    plat = platform.platform()
    host = platform.node()
    sys = platform.system()
    proc = platform.processor()
    print("Architecture: ", arch)
    print("Version: ", ver)
    print("Platform: ", plat)
    print("Hostname: ", host)
    print("System: ", sys)
    print("Processor: ", proc + '\n')
    with open('config.txt','a') as running_config:
        running_config.write('architecture = '+ arch + '\n'
                             'version = '+ ver + '\n'
                             'platform = '+ plat + '\n'
                             'hostname = '+ host + '\n'
                             'system = '+ sys + '\n'
                             'processor = '+ proc + '\n')
    print("Attributes written to config file.\n")

def check_serial():
    while True:
        g = input("Do you have a GPS device connected to a serial port? (y/n):\n")
        if g == 'y':
            print("Now going to scan for active serial ports...\n")
            return
        if g == 'n':
            print("Please connect a GPS device.")
            break
        else:
            print("Please press either 'y' or 'n'")

def scan_serial():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return(result)

def save_serial():
    print("Found active serial ports:")
    print(scan_serial())
    s = input("Please choose a COM port as displayed above:\n")
    open('config.txt','a').write('com = ' + s + '\n')

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

def verify_serial():
    print("Now going to verify GPS data...")
    print("Waiting for a valid GPS string...")
    print(readString())
    
def sentanceList():
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
    with open('config.txt','a') as running_config:
        running_config.write("sentances = ")
        for item in unique:
            running_config.write("%s," % item)
        running_config.write('\n')
    print("Sentance types saved to config")
    return(lines)
    
def getSentances():
    with open("config.txt") as f:
        for line in f:
            if "sentances" in line:
                sentanc = line.split("= ",1)[1]
                sentance = sentanc.rstrip(',\n\r')
                sentances = sentance.split(',')
                open("config.txt").close
    return(sentances)

##Actually works now?! WTF
def sentanceLengths():
    lengths = []
    x = 0
    while x < 20:
        string = readString()
        line = string.rstrip('\n\r')
        lines = line.split(",")
        segment = lines[0],len(lines)
        lengths.append(segment)
        unique = set(lengths)
        x += 1
    return(unique)

##Didn't expect this to work lels
def saveSentanceLengths():
    lengths = sentanceLengths()
    with open("config.txt",'a') as f:
        for i in lengths:
            x = i[0]
            y = i[1]
            f.write('%s = %s\n' %(x,y))
            print('%s = %s' %(x,y))
    f.close

def saveNumberSentances():
    sentances = getSentances()
    numbSent = len(sentances)
    with open("config.txt",'a') as f:
        f.write('totalSentances = %s\n' % numbSent)
    print("There are %s different sentances" % numbSent)

def create_database():
    i = input("Do you wish to manually specify database name? (y/n)\n")
    tables = getSentances()
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
    for i in tables:
        c.execute("CREATE TABLE IF NOT EXISTS %s (unix INT)" % (i))
        conn.commit()
    conn.close()
    with open('config.txt','a') as f:
        f.write('db = ' + db)
        f.close
    print("Tables created OK!")
    return(db)

#Holy fuck this is some mozart script right here:
def populateTables():
    db = create_database()
    conn = sqlite3.connect(db)
    c = conn.cursor()
    lengths = sentanceLengths()
    print("Populating tables...")
    for i in lengths:
        table = i[0]
        number = i[1]
        x = 1
        while x <= number:
            try:
                c.execute("ALTER TABLE %s ADD COLUMN '%s'" % (table, x))
            except:
                x += 1
                pass
    conn.commit()
    conn.close()
    print("Holy f@#%, it actually worked?!")

def raw_log():
    log_raw = 'log_raw.txt'
    log_raw_old = 'log_raw.txt.old'
    print("Looking for log_raw.txt file...")
    if os.path.exists(log_raw)==False:
        print("No existing raw gps log file, attempting to create one...")
        try:
            open(log_raw,'w')
            open(log_raw,'w').close
        except IOError:
            print("Unable to create file")
        print("Raw GPS log file created OK!")
    else:
        d = input("Raw GPS log file already exists, do you wish to backup and delete contents? (y/n)\n")
        if d == 'y':
            try:
                shutil.copyfile(log_raw,log_raw_old)
                print("Existing GPS raw log backed up.")
                open(log_raw,'w')
                print("GPS raw log now blank.\n")
            except IOError:
                print("Unable to read file.")
        elif d == 'n':
            input("No worries, raw gps log file left alone ;)")
        
    
def run(): 
    config_backup()
    check_time()
    check_system()
    check_serial()
    #scan_serial()
    save_serial()
    verify_serial()
    sentanceList()
    print(getSentances())
    saveSentanceLengths()
    saveNumberSentances()
    #create_database()
    populateTables()
    #raw_log()

run()
