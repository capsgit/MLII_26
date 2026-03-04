import sqlite3
import sys
import os
from pathlib import Path
from druckst_du import wait_for_keypress


def datenbank_erstellen():
    with sqlite3.connect("telefonbuch.db") as conn:
        c = conn.cursor()
        sql = """create table if not exists telefonbuch
                 (
                     id        integer
                         constraint id
                             primary key,
                     vorname   TEXT,
                     nachname  TEXT,
                     vorwahl   TEXT,
                     rufnummer TEXT
                 ) \
              """
        c.execute(sql)
        conn.commit()

    menu()


def cls():
    os.system('cls' if os.name=='nt' else 'clear')


def eintrag_suchen():
    pass


def eintrag_hinzufuegen():
    vorname = input("Vorname: ")
    nachname = input("Nachname: ")
    vorwahl = input("Vorwahl: ")
    rufnummer = input("Rufnummer: ")

    # Überprüfen, ob alles ausgefüllt ist:
    if not vorname or nachname or vorwahl or rufnummer:
        print("Bitte alle Angaben ausfüllen!")
        wait_for_keypress()
        cls()
        menu()

    params = (vorname, nachname, vorwahl, rufnummer)

    try:
        with sqlite3.connect("telefonbuch.db") as conn:
            c = conn.cursor()
            sql = """INSERT INTO telefonbuch (vorname, nachname, vorwahl, rufnummer) VALUES (?, ?, ?, ?)"""
            c.execute(sql, params)
            conn.commit()

        print("Eintrag erfolgreich hinzugefügt!")

    except Exception as e:
        print("Es ist ein Fehler aufgetreten: \n", e)

    finally:
        wait_for_keypress()
        cls()
        menu()

def eintrag_loeschen():
    pass


def alles_ausgeben():
    pass


def beenden():
    print("Auf Wiedersehen!")
    sys.exit(0)


def menu():
    items = ["Eintrag suchen", "Eintrag hinzufügen", "Eintrag löschen", "Alle Einträge anzeigen", "Beenden"]
    for i, item in enumerate(items, 1):
        print(f"{i} - {item}")

    auswahl = input("Bitte wählen Sie aus: ")

    match auswahl:
        case "1":
            eintrag_suchen()

        case"2":
            eintrag_hinzufuegen()

        case "3":
            eintrag_loeschen()

        case "4":
            alles_ausgeben()

        case "5":
            beenden()

if __name__ == "__main__":
    # Pfad-Variable abhängig vom Skriptordner erstellen:
    ordner = Path(__file__).parent
    db_name = ordner / "telefonbuch.db"
    datenbank_erstellen()
    menu()