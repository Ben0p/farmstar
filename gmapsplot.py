from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import config
import psycopg2
import gmplot

db = config.db
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
conn = sqlite3.connect(db)
c = conn.cursor()


# You can convert to float array in several ways
##r = np.array([1, 1, 2], dtype=np.float)
##s = np.array([float(i) for i in [1, 1, 2]])
##t = np.array([1, 2, 2]) * 1.0


def readDB():
    lat = []
    lon = []
    alt = []
    sql = "SELECT * FROM GPGGA"
    c.execute(sql)
    for row in c.fetchall(): 
        lat.append(row[3])
        lon.append(row[5])
        alt.append(row[10])
    return(lat,lon,alt)

def convert():
    data = readDB()
    lat = data[0]
    lon = data[1]
    alt = data[2]
    latc = []
    lonc = []
    altc = []
    for i in lat:
        x = i[:2].lstrip('0') + "." + "%.7s" % str(float(i[2:])*1.0/60.0).lstrip("0.")
        xf = str('-'+x)
        xfs = float(xf)
        latc.append(xfs)
    for i in lon:
        y = i[:3].lstrip('0') + "." + "%.7s" % str(float(i[3:])*1.0/60.0).lstrip("0.")
        yf = str(y)
        yfe = float(yf)
        lonc.append(yfe)
    for i in alt:
        x = i
        zf = str(x)
        altc.append(zf)
    return(latc,lonc,altc)
        
def plotGraph():
    data = convert()
    x = data[0]
    y = data[1]
    z = data[2]
    gmap = gmplot.GoogleMapPlotter(x[0],y[0],15)
    gmap.heatmap(x, y)
    gmap.draw('map.html')

plotGraph()
c.close()
conn.close()
        
