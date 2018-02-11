import os
import platform
import com
import serial



def setGlobals():
    global backdir
    global config
    global dicdir
    global host
    global comport

'''
#0 - Set globals
#1 - Get GPS com port
#2 - Get GPS time
#3 - Get NTP time (try)
#4 - Compare times
#5 - sync time if necessary
#6 - set path variables
#7 - create backup folder
#8 - backup config
#9 - backup database(s)



    


'''

def getCom():
    comport = com.scanSerial
     

def readSerial():
    ser = serial.Serial(comport,9600,timeout=1.5)
    line = ser.readline().decode('utf-8')
    sentence = line.rstrip('\n\r').split(',')
    return(sentence)


def gpsTime():
    while True:
        sentence = readSerial()
        if sentence[0] == 'GGA':
            fixtime = sentence[1]
            



def setPaths():
    backdir = os.path.join(os.path.dirname(__file__),
                           'backup',
                           datetime.now().strftime('%Y'),
                           datetime.now().strftime('%m'),
                           datetime.now().strftime('%H%M%S'))

    config = os.path.join(os.path.dirname(__file__),
                          'config.py')

    dicdir = os.path.join(os.path.dirname(__file__),
                          'dictionaries')



def backupFolder():
    try:
        os.makedirs(backdir)
    except:
        return(False)



def configBackup():
    if os.path.exists(config) == False:
        try:
            with open(config, 'w') as f:
                f.close
        except:
            return(False)
    else:
        try:
            backupFolder()
            shutil.copyfile(config, "%s/%s" % (backdir, 'config.py'))
            with open(config,'w') as f:
                f.close
        except:
            return(False)



            
        
        
