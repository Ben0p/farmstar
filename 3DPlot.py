from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import config

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
        xf = float(x)
        latc.append(xf)
    for i in lon:
        y = i[:3].lstrip('0') + "." + "%.7s" % str(float(i[3:])*1.0/60.0).lstrip("0.")
        yf = float(y)
        lonc.append(yf)
    for i in alt:
        x = i
        zf = float(x)
        altc.append(zf)
    return(latc,lonc,altc)
        
def plotGraph():
    data = convert()
    x = data[0]
    y = data[1]
    z = data[2]
    ax.plot_wireframe(x,y,z)
    ax.set_xlabel("lat")
    ax.set_ylabel("lon")
    ax.set_zlabel("alt")
    plt.show()

plotGraph()
#convert()
        
