import json
import sqlite3
import re


con = sqlite3.connect('xim.db')
c = con.cursor()


feature = {"geometry": {"type": "Point", "coordinates": []}, "type": "Feature", "properties": {}}
    


def getData():
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    features = []
    for table in tables:
        match = re.search('''(?<=')\s*[^']+?\s*(?=')''',str(table))
        name = match.group().strip()
        c.execute("SELECT * FROM %s ORDER BY UNIX DESC LIMIT 1" % (name))
        result = c.fetchone()
        if result != None:
            lat = result[6]
            lon = result[7]
            feature['geometry']['coordinates'] = [lon,lat]
            features.append(feature)
            geojson = ''.join(str(e)+',' for e in features)
            j = json.dumps(geojson)
    return(j)


if __name__ == '__main__':
    print(getData())
