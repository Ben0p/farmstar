import time
import datetime

ut = time.time()
dt = str(datetime.datetime.fromtimestamp(ut).strftime('%d/%m/%Y %H:%M:%S'))

def printTime():
    while True:
        global dt
        print(dt)
        time.sleep(1)

printTime()
