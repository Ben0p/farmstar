import time
import datetime
import pytz
import tzlocal

while True:
    epoc = time.time()
    zone = time.timezone
    local_tz = tzlocal.get_localzone()
    utc = datetime.datetime.utcnow()
    timestring = datetime.datetime.fromtimestamp(epoc).strftime('%Y%m%d%H%M%S%f')[:-3]
    print("Epoc Time: ", epoc)
    print("Epoc Timezone: ", zone)
    print("Local Time: ", timestring)
    print("Timezone: ", local_tz)
    print("UTC: ", utc)
    time.sleep(1)
