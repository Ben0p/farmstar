import time
import serial

def open_comport():
    with open("config.txt") as f:
        for line in f:
            if "com" in line:
                comport = line.split("= ",1)[1]
                ser = serial.Serial(comport,9600,timeout=1) # Open Serial port
                open("config.txt").close
    return(ser)

def readString():
    ser = open_comport()
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
            
def raw_log():
    log_raw = 'serial_test.txt'
    try:
        with open(log_raw,"a") as f:
            f.write(readString())
    except:
        print("Computer syas no :(")

create_raw_log()
while True:
    raw_log()
    print(readString())
