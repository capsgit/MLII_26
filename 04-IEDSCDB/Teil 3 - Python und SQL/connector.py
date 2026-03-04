import mysql.connector as mc

conn = None

# generra la conexion con el SQL
try:
    conn = mc.connect(host = "localhost", user = "root",
                      #        👹👹👹👹👹👹👹👹!!!
                      passwd = "FCbarcelona2025 !")

except mc.Error as e:
    print("Error connecting to MySQL server: \n", e)


# test si existe conexion
"""
if conn.is_connected():
    print("connectado")
else:
    print("no connectado")
"""


# cursor
cursor = conn.cursor()
print(cursor)

# crear DB nueva desde el servidor de MySQL
try:
    cursor.execute("CREATE DATABASE IF NOT EXISTS telefonbuch")
except mc.Error as e:
    print("Error creating database: \n", e)