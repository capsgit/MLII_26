import sqlite3

connection = sqlite3.connect("telefonbuch.db") # Genera la conexion
cursor = connection.cursor() # se genera un cursor con acceso al db


var_vorname = "Alex"
var_nachname = "Piñeros"
var_vorwahl = "0166"
var_rufnummer = "0000000"

# la orden/Befehl-SQL SE GUARDA en una variable ("sql")
params = (var_vorname, var_nachname, var_vorwahl, var_rufnummer) # importante el orden, en tuppel

sql = """INSERT INTO telefonbuch (vorname, nachname, vorwahl, rufnummer) VALUES (?, ?, ?, ?)"""

#sql = """create table telefonbuch
#          (
#              id        integer
#                  constraint id
#                      primary key,
#              vorname   TEXT,
#              nachname  TEXT,
#              vorwahl   TEXT,
#              rufnummer TEXT
#          )
#      """

cursor.execute(sql, params) # "sql" run
connection.commit() # se confirma la orden/Befehl de nuevo (necesario)
connection.close() # se cierra la conexion


