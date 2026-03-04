
import mysql.connector as mc
import hashlib

from pwinput import pwinput

conn = None
result = None

try:
    conn = mc.connect(host="localhost",
                            user="root",
                            passwd="FCbarcelona2025 !",
                            database="benutzer", # solo despues de haberla creado
                            use_pure=True)


except mc.errors.ProgrammingError:
    print("Es ist ein Fehler bei der Verbindung zur Datenbank aufgetreten!")

cursor = conn.cursor()

name = input("escribe tu nombre: ")
passwort = pwinput("Passwort: ", mask='*')
# salt = os.urandom(32)

params = (name, )

sql = """SELECT passwort, salt FROM benutzer WHERE benutzername = %s"""

try:
    cursor.execute(sql, params)
    result = cursor.fetchone()
    print(result)

except mc.Error as err:
    print("Es ist ein Fehler aufgetreten: \n", err)

finally:
    if conn.is_connected():
        conn.close()

if result:
    result
    db_passwort = bytes.fromhex(result[0])
    db_salt = bytes.fromhex(result[1])

else:
    print("Benutzer nicht gefunden")

key = hashlib.pbkdf2_hmac('sha256',
                    passwort.encode('utf-8'),
                    db_salt,
                   1000) # mejor 100.000 iteraciones

if login(name, passwort):
    print("Bienvenido")
else:
    print("Password Incorrecto")