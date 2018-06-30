import serial
import sys
import glob
import fs_checksum
from dicts import PORTS, MESSAGE, TALKER


def ports(ports=None):
    """
    Scans for active serial ports and then checks those for GPS data, returning a dictionary.
    Optionally pass a list of serial ports to test. eg ["COM1","COM5"]
    """

    def scan():
        active = []
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        for port in ports:
            try:
                print("Testing port %s" % (port))
                ser = serial.Serial(port, 9600, timeout=1.5)
                for _ in range(5):
                    ser.readline().decode("utf-8")
                ser.close()
                active.append(port)
            except (OSError, serial.SerialException):
                pass
        print("Active ports = {}".format(active))
        port_list['active'] = active
        return(active)

    def test(ports):
        for port in ports:
            print("Scanning port %s for GPS data..." % (port))
            ser = serial.Serial(port, 9600, timeout=1.5)  # open serial port
            count = 0
            for _ in range(5):  # read 5 lines only (loop code 5 times)
                # read serial line
                line = ser.readline().decode("utf-8")
                # Remove newline
                stripped = line.rstrip('\n\r')
                # Split into a list format
                sentence = stripped.split(",")
                # Get the message type
                message = sentence[0][3:]
                # Get the talker type
                talker = sentence[0][1:3]

                for key in TALKER.TALKER.keys():
                    if talker == key:
                        count += 1
                        print('{} = {}'.format(key, talker))
                        break
            if count == 5:
                port_list['gps'].append(port)
            else:
                port_list['unknown'].append(port)
        return(port_list)
                

    port_list = PORTS.LIST
    if ports is None:
        ports = scan()
    test(ports)
    return(port_list)



if __name__ == '__main__':
    ports = ports()
    print(ports)
    gps_ports = ports['gps']
    print('GPS Ports: {}'.format(gps_ports))
    # Ports(["COM1","COM3","COM5"])
