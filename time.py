import time
import datetime

while True:
    epoc = time.time()
    zone = time.timezone
    timestring = datetime.datetime.fromtimestamp(epoc).strftime('%Y%m%d%H%M%S%f')
    print("Epoc time: ", epoc)
    print("Timezone: ", zone)
    print("UTC Time: ", timestring)
    time.sleep(1)
