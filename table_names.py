import sqlite3

def db_name():
    with open("config.txt") as f:
        for line in f:
            if "db" in line:
                l = line.split("= ",1)[1]
                db = l.rstrip('\n\r')
                open("config.txt").close
    return(db)

def getTables():
    t = []
    db = db_name()
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('select name from sqlite_master where type=\'table\'')
    for table in c:
        t.append(table[0])
    return(t)

print(getTables())
