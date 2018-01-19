import serial
import time
import os
import sys
import sqlite3
import datetime
import config

db = config.db
maxlist = config.maxlist
sqlint = 10
comport = config.comport

def serialStream():
    lines = ['']
    ser = None
    loopcount = 0
    starttime = time.time()
    try:
        if os.path.exists(db)==False
        conn = sqlite3.connect(db)
        c = conn.cursor()
    except:
        print("Failed to connect to database '%s'" % (db))
    while True:
        try:
            if(ser == None or lines[0] == ''):
                ser = serial.Serial(comport,9600,timeout=1.5)
                print("Reconnecting to %s" % (comport))
            line = ser.readline().decode("utf-8") # Read the entire string
            lines = line.rstrip('\n\r').split(",")
            try:
                livePos(lines)
                #logDB(lines)
            except:
                print("Live position fail")
        except:
            if(not(ser == None)):
                ser.close()
                ser = None
                print("Disconnecting")
            print("No Connection to %s" % (comport))
            time.sleep(2)
        
def livePos(sentence):
        try:
            if sentence[0][3:] == 'GGA':
                lat = sentence[2]
                lon = sentence[4]
                x = lat[:2].lstrip('0') + "." + "%.7s" % str(float(lat[2:])*1.0/60.0).lstrip("0.")
                if sentence[3] == 'S':
                    xf = str('-'+x)
                else:
                    xf = str(x)
                y = lon[:3].lstrip('0') + "." + "%.7s" % str(float(lon[3:])*1.0/60.0).lstrip("0.")
                yf = str(y)            
                with open('live.geojson','w') as f:
                    f.write('{"geometry": {"type": "Point", "coordinates": [%s, %s]}, "type": "Feature", "properties": {}}' % (yf, xf))
                print(yf,xf)
            else:
                #return("Invalid String")
                pass
        except:
            return("Epic Fail")
        
def logDB(sentence):
    while True:
        lines = stringGen()
        while lines:
            lines = stringGen() # There is a reason this is here twice, can't remember why
            length = len(lines)
            table = lines[1]
            unix = time.time()
            for i in maxlist:
                if i[0] == lines[1]:
                    if i[1]+1 == length:
                        var_string = ', '.join('?' * length)
                        query_string = 'INSERT INTO %s VALUES (%s);' % (table, var_string)
                        c.execute(query_string ,lines)
                        #print('=',lines)
                    elif i[1]+1 > length:
                        diff = i[1]+1-length
                        checksum = lines[-1]
                        slicedstring = lines[:-1]
                        extendedstring = []
                        extendedstring = slicedstring
                        for _ in range(diff):
                            extendedstring.append('')
                        finalstring = []
                        finalstring = extendedstring
                        finalstring.append(checksum)
                        length = len(finalstring)
                        var_string = ', '.join('?' * length)
                        query_string = 'INSERT INTO %s VALUES (%s);' % (table, var_string)
                        c.execute(query_string ,finalstring)                        
                        #print('+',finalstring)
                    elif i[1]+1 < length:
                        print("less, script failure :(")
            timer = unix - starttime
            if timer >= sqlint:
                conn.commit()
                starttime = time.time()
                timer = 0
                print("commit")
    conn.commit()
    print("commit")
    print("End of file")
            
serialStream()
