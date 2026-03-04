from pathlib import Path
import sqlite3
import sys
import os

DB_PATH = Path(__file__).with_name("telefonbuch.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS telefonbuch (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vorname TEXT NOT NULL,
            nachname TEXT NOT NULL,
            vorwahl TEXT NOT NULL,
            rufnumer TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def cls():
    """Funktioniert bei Windows, Linux, Unix und Mac"""
    os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    print("Telefonbuch")
    print("Bitte wählen Sie...")
    print("1 - Eintrag hinzufügen")
    print("2 - Eintrag suchen")
    print("3 - Eintrag löschen")
    print("4 - Alle Einträge anzeigen")
    print("5 - Eintrag aktualisieren")
    print("e - Ende")

    auswahl = input("Ihre Auswahl: ")

    if auswahl == "1":
        eintrag_hinzufuegen()
    elif auswahl == "2":
        nummer_ausgeben()
    elif auswahl == "3":
        nummer_loeschen()
    elif auswahl == "4":
        liste_ausgeben()
    elif auswahl == "5":
        eintrag_aktualisieren()

    elif auswahl == "e":
        sys.exit(0)

def eintrag_hinzufuegen():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    vorname = input("Bitte geben Sie den Vornamen ein: ")
    nachname = input("Bitte geben Sie den Nachnamen ein: ")
    vorwahl = input("Bitte geben Sie den Vorwahl ein: ")
    rufnummer = input("Bitte geben Sie die Rufnummer ein: ")

    params = (vorname, nachname, vorwahl, rufnummer)

    sql = """INSERT INTO telefonbuch(vorname, nachname, vorwahl, rufnummer) VALUES(?,?,?,?)"""

    c.execute(sql, params)
    conn.commit()
    conn.close()
    print("Eintrag hinzugefügt")
    menu()


def nummer_ausgeben():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    vname = input("Bitte geben Sie den Vornamen ein: ") + "%"
    nname = input("Bitte geben Sie den Nachnamen ein: ") +"%"
    params = (vname, nname)
    sql = """SELECT * FROM telefonbuch WHERE vorname like ? AND nachname like ?"""
    c.execute(sql, params)
    ausgabe = c.fetchall()
    conn.close()

    for _, v, n, r in ausgabe:
        print()
        print(f"Vorname: {v} Nachname: {n} Rufnummer: {r}")
    # wait_for_keypress()
    # cls()
    menu()


def nummer_loeschen():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    nname = input("Bitte geben Sie den Nachnamen ein: ") + "%"
    params = (nname, )
    sql = """SELECT * FROM telefonbuch WHERE nachname like (?)"""
    c.execute(sql, params)
    ausgabe = c.fetchall()

    for a in ausgabe:
        print()
        print(f"ID: {a[0]} Vorname: {a[1]:.20s} Nachname: {a[2]:.20s} Rufnummer: {a[3]}")

    dele = input("Welchen Eintrag möchten Sie löschen? Bitte geben Sie die ID an: ")
    params = (dele, )
    sql = """DELETE FROM telefonbuch WHERE ID = ?"""
    try:
        c.execute(sql, params)
        conn.commit()
        print("Eintrag erfolgreich gelöscht!")


    except Exception as e:
        print("Es ist ein Fehler aufgetreten:", e)

    finally:
        conn.close()
        menu()


def liste_ausgeben():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    sql = """SELECT * FROM telefonbuch """
    c.execute(sql)
    ausgabe = c.fetchall()
    conn.close()

    print()
    print("Vorhandene Einträge:")
    print(f"{'ID':<4} {'Vorname':<15} {'Nachname':<15} {'Vorwahl':<8} {'Rufnummer':<15}")
    print("-" * 50)

    for i, v, n, w, r in ausgabe:
        print(f"{i:<4} {v:<15} {n:<15} {w:<8} {r:<15}")
    menu()


def eintrag_aktualisieren():
    vorname_neu = ""
    nachname_neu = ""
    vorwahl_neu = ""
    rufnummer_neu = ""

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    nname = input("Bitte geben Sie den Nachnamen ein: ") + "%"
    params = (nname,)
    sql = """SELECT * \
             FROM telefonbuch \
             WHERE nachname like (?)"""
    c.execute(sql, params)
    ausgabe = c.fetchall()

    for i, v, n, r in ausgabe:
        print(i, v, n, r)

    auswahl = input("Welchen Eintrag möchten Sie aktualisieren? \nBitte geben Sie die ID ein: ")

    params = (auswahl,)

    sql = """SELECT * \
             FROM telefonbuch \
             WHERE id = ?"""

    c.execute(sql, params)
    ausgabe = c.fetchone()  # Es wird nur ein Eintrag erwartet

    _, vorname_alt, nachname_alt, vorwahl_alt, rufnummer_alt = ausgabe

    vorname_neu = input(f"Bitte geben Sie den neuen Vornamen ein ({vorname_alt}): ")
    nachname_neu = input(f"Bitte geben Sie den neuen Nachnamen ein ({nachname_alt}): ")
    vorwahl_neu = input(f"Bitte geben Sie den neuen Vorwahlnummer ein ({vorwahl_alt}): ")
    rufnummer_neu = input(f"Bitte geben Sie die neue Rufnummer ein ({rufnummer_alt}): ")

    if vorname_neu == "":
        vorname_neu = vorname_alt

    if nachname_neu == "":
        nachname_neu = nachname_alt

    if vorwahl_neu == "":
        vorwahl_neu = vorwahl_alt

    if rufnummer_neu == "":
        rufnummer_neu = rufnummer_alt

    params = (vorname_neu, nachname_neu, rufnummer_neu, vorwahl_neu)
    sql = """UPDATE telefonbuch \
             SET vorname = ?, nachname = ?, vorwahl = ?, rufnummer = ? \
             WHERE id = ?"""
    c.execute(sql, params)
    conn.commit()
    print("Eintrag aktualisiert")
    menu()

print("Usando DB:", DB_PATH.resolve())
if __name__ == "__main__":
    init_db()
    menu()