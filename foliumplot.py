from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import config
import psycopg2
import gmplot
import folium
import json
from folium.plugins import HeatMap
from folium.features import CustomIcon
from PIL import Image



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

def points():
    data = convert()
    x = data[0]
    y = data[1]
    z = data[2]
    points = list(zip(x, y))
    return(points)

def tractor_blue():
    img = Image.open('Tractor-Blue.png')
    img_rot = img.rotate(45, expand=True)
    img_rot.save('Tractor-Blue_rot.png')
    icon_image = 'Tractor-Blue_rot.png'
    icon_size =(32,32)
    icon_anchor = (16,31)
    angle = 'angle=45'
    icon = CustomIcon(icon_image, icon_size, icon_anchor)
    return(icon)
    
    
    

def plotMap():
    icon = tractor_blue()
    #Gather data
    point_list = points()
    last_point = point_list[-1]
    #Generate base map position and zoom
    my_map = folium.Map(location=[last_point[0], last_point[1]], zoom_start=18)
    #Create Groups
    track_group = folium.FeatureGroup(name='Track')
    marker_group = folium.FeatureGroup(name='Marker')
    heat_group = folium.FeatureGroup(name='Heat Map')
    vector_group = folium.FeatureGroup(name='Vector')
    icon_group = folium.FeatureGroup(name='icon')
    #Set marker positions
    folium.Marker(location=[last_point[0], last_point[1]], popup='Latest').add_to(marker_group)
    #Test Polygon Marker
    folium.features.RegularPolygonMarker(location=[last_point[0], last_point[1]], color='black',opacity=1,weight=2,fill_color='blue',fill_opacity=1,number_of_sides=3,rotation=0,radius=15,popup=None).add_to(vector_group)
    #Test Custom Icon
    folium.Marker(location=[last_point[0], last_point[1]], icon=icon).add_to(icon_group)
    #Add base map tiles layers
    folium.TileLayer('cartodbdark_matter').add_to(my_map)
    folium.TileLayer('stamenterrain').add_to(my_map)
    folium.TileLayer('stamentoner').add_to(my_map)
    folium.TileLayer('stamenwatercolor').add_to(my_map)
    folium.TileLayer('cartodbpositron').add_to(my_map)
    #Add groups to map
    track_group.add_to(my_map)
    marker_group.add_to(my_map)
    heat_group.add_to(my_map)
    vector_group.add_to(my_map)
    icon_group.add_to(my_map)
    #Add data to layer groups
    HeatMap(point_list).add_to(heat_group)
    folium.PolyLine(point_list).add_to(track_group)
    #Add layer control
    folium.LayerControl().add_to(my_map)
    #Save to file
    my_map.save('201711041430_DarkMatter.html')

plotMap()
c.close()
conn.close()
        
