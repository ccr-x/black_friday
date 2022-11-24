import mariadb as mdb

conn = mdb.connect(user="root", password="raspberry", database="raspberrypi")

print(conn)
