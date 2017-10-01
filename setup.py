import sqlite3
import time
import datetime
import serial
import sys
import shutil
import glob
import pathlib
import platform
import os
import socket
import pytz
import tzlocal

config = 'config.py'
oldconfig = 'config.py.old'
timezone = tzlocal.get_localzone()
epocoffset = time.timezone
comportlist = []
comport = 'x'
sentencetypes = []
db = 'x'
conn = sqlite3.connect(db)
c = conn.cursor()
sentencelengths = []
openserial = 'x'

def configBackup():
    global config
    global oldconfig
    print("This script will generate a config file 'config.py'")
    print("If file exists, it will be moved to 'config.py.old'")
    print("If 'config.py.old' exists, it will be overwritten!")
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
    if os.path.exists(config)==False:
        print("No config file exists, attempting to create one...")
        try:
            open(config,'w')
            open(config,'w').close
        except IOError:
            print("Unable to create file")
        print("Blank config file created OK!")
    else:
        try:
            shutil.copyfile(config, oldconfig)
            print("Existing config backed up.")
            open(config,'w')
            print("Config now blank.\n")
        except IOError:
            print("Unable to read file.")

def timeNow():
    epoc = time.time()
    timenow = str(datetime.datetime.fromtimestamp(epoc).strftime('%d/%m/%Y %H:%M:%S'))
    return(epoc,timenow)
    
def checkTime():
    global timezone
    global epocoffset
    global config
    while True:
        timenow = timeNow()
        datetime = timenow[1]
        print(datetime)
        print(timezone)
        t = input("Is this the correct time and zone? (y/n):\n")
        if t == 'y':
            with open(config,'a') as f:
                f.write('created = %s\n'
                        'timezone = %s\n'
                        'epocoffset = %s\n'
                        % (datetime, timezone, epocoffset))
            
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
        
def getSystem():
    global config
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
    with open(config,'a') as f:
        f.write('architecture = '+ arch + '\n'
                'version = '+ ver + '\n'
                'platform = '+ plat + '\n'
                'hostname = '+ host + '\n'
                'system = '+ sys + '\n'
                'processor = '+ proc + '\n')
    print("Attributes written to config file.\n")

def checkSerial():
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

def scanSerial():
    global comportlist
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
    comportlist = result

def saveSerial():
    global comportlist
    global config
    print("Found active serial ports:")
    print(comportlist)
    s = input("Please choose a COM port as displayed above:\n")
    open(config,'a').write('com = ' + s + '\n')

def openComport():
    global comport
    global config
    global openserial
    with open(config) as f:
        for line in f:
            if "com" in line:
                port = line.split("= ",1)[1]
                comport = port.rstrip('\n\r')
                openserial = serial.Serial(comport,9600,timeout=1) # Open Serial port
                f.close

def serialStream():
    global openserial
    while True:
        while openserial.read().decode("utf-8") != '$': # Wait for the begging of the string
            pass # Do nothing
        serialstream = openserial.readline().decode("utf-8") # Read the entire string
        return(serialstream)

def verifySerial():
    print("Now going to verify GPS data...")
    print("Waiting for a valid GPS string...")
    print(serialStream())

def serialStreamList():
    string = serialStream()
    line = string.rstrip('\n\r')
    lines = line.split(",")
    return(lines)
    
def saveSentenceTypes():
    global config
    types = []
    x = 0
    print("Scanning for unique GPS sentences...")
    while x < 20:
        lines = serialStreamList()
        sentence = lines[0]
        types.append(sentence)
        unique = set(types)
        x += 1
    with open(config,'a') as f:
        f.write("sentencetypes = ")
        for i in unique:
            f.write("%s," % i)
        f.write('\n')
    print("Sentence types saved to config")
    
def getSentenceTypes():
    global config
    global sentencestypes
    with open(config) as f:
        for l in f:
            if "sentencetypes" in l:
                senten = l.split("= ",1)[1]
                sentenc = senten.rstrip(',\n\r')
                sentencetypes = sentenc.split(',')
                f.close

##Actually works now?! WTF
def sentanceLengths():
    global sentencelengths
    lengths = []
    x = 0
    while x < 20:
        sl = streamSerialList()
        segment = sl[0],len(sl)
        lengths.append(segment)
        unique = set(lengths)
        x += 1
    sentencelengths = unique

##Didn't expect this to work lels
def saveSentenceLengths():
    global sentencelengths
    global config
    with open(config,'a') as f:
        for i in sentencelengths:
            x = i[0]
            y = i[1]
            f.write('%s = %s\n' %(x,y))
            print('%s = %s' %(x,y))

def saveNumberSentences():
    global config
    global sentencetypes
    numbSent = len(sentencetypes)
    with open(config,'a') as f:
        f.write('totalSentences = %s\n' % numbSent)
    print("There are %s different sentences" % numbSent)

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
    print("Connected to '"+db+"' OK!")
    for i in sentencetypes:
        c.execute("CREATE TABLE IF NOT EXISTS %s (unix INT)" % (i))
        conn.commit()
    with open(config,'a') as f:
        f.write('db = ' + db)
        f.close
    print("Tables created OK!")

#Holy fuck this is some mozart script right here:
def populateTables():
    global db
    global conn
    global c
    global sentencelengths
    print("Populating tables...")
    for i in sentencelengths:
        sentnace = i[0]
        length = i[1]
        x = 1
        while x <= length:
            try:
                c.execute("ALTER TABLE %s ADD COLUMN '%s'" % (sentence, x))
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
    configBackup()
    checkTime()
    getSystem()
    checkSerial()
    scanSerial()
    saveSerial()
    openComport()
    verifySerial()
    saveSentenceTypes()
    getSentenceTypes()
    print(sentencetypes)
    saveSentenceLengths()
    saveNumberSentences()
    createDatabase()
    populateTables()
    #raw_log()

run()
