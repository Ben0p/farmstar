import serial
import time
import os
import sys
import sqlite3
import datetime
try:
    import config
except:
    print("No config")


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
