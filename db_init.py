from sqlite3 import connect

conn = connect("data.db")
try:
    conn.execute("CREATE TABLE STAT(STATUS TEXT)")
    conn.execute("INSERT INTO STAT VALUES(?)", ("f",))
    conn.commit()
except:
    pass
finally:
    conn.close()