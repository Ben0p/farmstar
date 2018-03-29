import serial
import time


class stream():

    def __init__(self,port=None):
        if port == None:
            self.status = "No port specified"
        else:
            self.port = port
            self.ser = None
            self.line = ''
            self.status = "Initializing..."
            self.data()
            self.status = "Failed to initialize serial stream"
            

    def data(self):
        while True:
            try:
                if(self.ser == None or self.line == ''):
                    self.ser = serial.Serial(self.port,9600,timeout=1.5)
                    self.status = "Reconnecting..."
                self.line = self.ser.readline().decode("utf-8")
                print(self.line)
                self.status = "Streaming data..."
            except:
                if(not(self.ser == None)):
                    self.ser.close()
                    self.ser = None
                    self.status = "Disconnecting..."
                self.status = str("No Connection to %s" % (self.port))
                self.status = "Sleep 2 seconds"
                time.sleep(2)
                
                
        





if __name__ == '__main__':
    import com
    comport = com.Ports().active
    stream(comport[0])
    #print(stream.status)
