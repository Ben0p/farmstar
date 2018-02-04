import nmea



while True:
    lat = nmea.GGA['Latitude']
    lon = nmea.GGA['Longitude']
    print(lat,lon)
