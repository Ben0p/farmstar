import time
from dateutil import tz
from datetime import datetime
from dicts import GPS, GSA, GGA, STATUS, CHECK, SPACE
import fs_checksum
import fs_time
import fs_com
import fs_serial
import serial
import copy


'''
Farmstar nmea data parser
Converts GPS data into a bunch of dictionaries
Creates a dictionary of all dictionaries
'''


class parse():

    # parse raw nmea data (one line at a time)

    def __init__(self):
        self.GPS = GPS.GPS
        self.STATUS = STATUS.STATUS
        self.GGA = GGA.GGA
        self.GSA = GSA.GSA
        self.GSAALL = GSA.ALL

    def parseLine(self, line=None):
        self.line = line
        if self.line == None:
            print("No data recieved")
        else:
            # Remove newline
            self.stripped = self.line.rstrip('\n\r')
            # Split into a list format
            self.sentence = self.stripped.split(",")
            # Get the message type
            self.message = self.sentence[0][3:]
            # Get the talker type
            self.talker = self.sentence[0][1:3]
            # NMEA type
            self.nmea = self.sentence[0][1:6]

            self.parseSTATUS()

            if self.message == 'GGA':
                self.parseGGA()
            elif self.message == 'GSA':
                self.parseGSA()
            else:
                pass
            return(self.GPS)

    def parseSTATUS(self):
        # Send to checksum parser
        self.CHECKSUM = fs_checksum.parse(self.line)

        # Overall status
        self.STATUS['status'] = 'Doing Stuff'
        self.STATUS['string'] = self.stripped
        self.STATUS['sentence'] = self.sentence
        self.STATUS['talker'] = self.talker
        self.STATUS['message'] = self.message
        self.STATUS['nmea'] = self.nmea
        self.STATUS['check'] = self.CHECKSUM['status']
        self.STATUS['valid'] = self.CHECKSUM['valid']
        self.STATUS['checksum'] = self.CHECKSUM['checksum']
        self.STATUS['calculated'] = self.CHECKSUM['calculated']
        self.STATUS['count_total'] += 1

        if self.STATUS['valid'] == True:
            self.STATUS['count_good'] += 1
        else:
            self.STATUS['count_bad'] += 1

        self.STATUS['bad_percent'] = int(
            round((int(self.STATUS['count_bad'])/int(self.STATUS['count_total']))*100))
        self.GPS['STATUS'] = self.STATUS

    def parseGGA(self):
        # Count the total/good/bad strings
        self.GGA['Count_total'] += 1
        if self.CHECKSUM['valid'] == True:
            self.GGA['Count_good'] += 1
        else:
            self.GGA['Count_bad'] += 1

        self.SPACETIME = fs_time.parse(self.sentence[1]).SPACETIME

        self.GGA['Fix'] = self.SPACETIME['fixutc']
        self.GGA['Local_time'] = self.SPACETIME['localtime']
        self.GGA['Age'] = self.SPACETIME['age']
        self.GGA['String'] = self.stripped
        self.GGA['Sentence'] = self.sentence
        self.GGA['Talker'] = self.sentence[0][3:]
        self.GGA['Message'] = self.sentence[0][1:3]
        self.GGA['NMEA'] = self.nmea
        self.GGA['Checksum'] = self.CHECKSUM['checksum']
        self.GGA['Calculated'] = self.CHECKSUM['calculated']
        self.GGA['Check'] = self.CHECKSUM['status']

        # Latitude conversion
        self.lat = self.sentence[2][:2].lstrip(
            '0') + "." + "%.7s" % str(float(self.sentence[2][2:])*1.0/60.0).lstrip("0.")
        if self.sentence[3] == 'S':
            self.GGA['Latitude'] = float(self.lat)*-1
        else:
            self.GGA['Latitude'] = float(self.lat)
        self.GGA['North/South'] = self.sentence[3]

        # Lonitude conversion
        self.lon = self.sentence[4][:3].lstrip(
            '0') + "." + "%.7s" % str(float(self.sentence[4][3:])*1.0/60.0).lstrip("0.")
        self.GGA['Longitude'] = float(self.lon)
        self.GGA['East/West'] = self.sentence[5]

        # GGA Quality
        self.GGA['Quality'] = self.sentence[6]
        self.QUA = {'': 'None',
                    '0': 'Invalid',
                    '1': 'GPS Fix',
                    '2': 'DGPS Fix',
                    '3': 'PPS Fix',
                    '4': 'RTK',
                    '5': 'Float RTK',
                    '6': 'Estimated',
                    '7': 'Manual',
                    '8': 'Simulation',
                    }

        self.GGA['Type'] = self.QUA[self.GGA['Quality']]

        # GGA Other
        self.GGA['Satellites'] = self.sentence[7]
        self.GGA['Accuracy'] = self.sentence[8]
        self.GGA['Altitude'] = float(self.sentence[9])
        self.GGA['Altitude_Units'] = self.sentence[10]
        self.GGA['GeoID_Height'] = self.sentence[11]
        self.GGA['GeoID_Units'] = self.sentence[12]

        # Pack SPACETIME and GGA dictionaries into GPS dictionary
        self.GPS['SPACETIME'] = self.SPACETIME
        self.GPS['GGA'] = self.GGA
        self.GPS['CHECKSUM'] = self.CHECKSUM

    def parseGSA(self):
        self.GSA['Count_total'] += 1
        if self.CHECKSUM['valid'] == True:
            self.GSA['Count_good'] += 1
        else:
            self.GSA['Count_bad'] += 1

        self.GSA['string'] = self.stripped
        self.GSA['sentence'] = self.sentence
        self.GSA['talker'] = self.talker
        self.GSA['message'] = self.message
        self.GSA['nmea'] = self.sentence[0][1:6]
        self.GSA['a/m'] = self.sentence[1]
        self.SEL = {'': 'None',
                    'A': 'Auto',
                    'M': 'Manu',
                    }
        self.GSA['selection'] = self.SEL[self.GSA['a/m']]
        self.GSA['type'] = str(self.sentence[2])
        self.MOD = {'': 'No',
                    '1': '0D',
                    '2': '2D',
                    '3': '3D',
                    }
        self.GSA['mode'] = self.MOD[self.GSA['type']]
        if self.sentence[3] == '':
            self.GSA['PRNs'] = '   '
        else:
            self.GSA['PRNs'] = self.sentence[3]

        if self.sentence[-3] == '':
            self.GSA['PDOP'] = '   '
        else:
            self.GSA['PDOP'] = self.sentence[-3]

        if self.sentence[-2] == '':
            self.GSA['HDOP'] = '   '
        else:
            self.GSA['HDOP'] = self.sentence[-2]

        if self.sentence[-1][-8:-3] == '':
            self.GSA['VDOP'] = '   '
        else:
            self.GSA['VDOP'] = self.sentence[-1][-8:-3]

        self.GSA['checksum'] = self.CHECKSUM['checksum']

        # Create a list of the different GSA talkers
        gsalist = self.GSAALL['list']
        # Append current GSA talker
        gsalist.append(self.nmea)
        # Unique items only
        gsalist = list(set(gsalist))
        # Sort alphabetically so it's always the same order
        gsalist.sort()
        # Write list back to dictionary
        self.GSAALL['list'] = gsalist

        # Need to do deepcopy
        self.GSAALL[self.nmea] = copy.deepcopy(self.GSA)

        # Write current GSA dictionary to the GSAALL dictionary
        self.GSAALL['GSA'] = self.GSA

        # Write the GSAALL dictionary to the GPS dictionary
        self.GPS['GSA'] = self.GSAALL


if __name__ == '__main__':

    ports = fs_com.ports()
    port = ports['gps'][0]
    serial = fs_serial.stream(port)
    nmea = parse()
    while True:
        serial_data = serial.data()
        serial_line = serial_data['line']
        serial_status = serial_data['status']
        gps_data = nmea.parseLine(serial_line)
        print(gps_data)
        print('')

