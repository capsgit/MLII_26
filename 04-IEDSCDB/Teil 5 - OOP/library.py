import sqlite3
import os
from pathlib import Path
from pyfiglet import Figlet


class Buch:
    def __init__(self, titel, autor, ort):
        self.titel = titel
        self.autor = autor
        self.lagerort = ort


class Bibliothek:
    def __init__(self, database):
        self.datenbank = database

    def buch_hinzufuegen(self, buch):
        c = self.datenbank.verbindung.cursor()
        params = (buch.titel, buch.autor, buch.lagerort)
        c.execute("INSERT INTO buecher VALUES (NULL, ?, ?, ?)", params)
        self.datenbank.verbindung.commit()

    def alle_bucher_ausgeben(self):
        c = self.datenbank.verbindung.cursor()
        c.execute("SELECT * FROM buecher")
        for i, titel, author, ort in c:
            print(f"{i}  {titel} - {author}  {ort}")

    def buch_suchen(self, titel):
        c = self.datenbank.verbindung.cursor()
        params = ("%" + titel + "%",)
        c.execute("SELECT * FROM buecher WHERE titel like ?", params)

        for i, titel, author, ort in c:
            print(f"{i}  {titel} - {author}  {ort}")


class Datenbank:
    def __init__(self, pfad):
        self.pfad = pfad
        self.verbindung = None
        self.ist_neu = not os.path.exists(self.pfad)
        self.verbindung_herstellen()

    def verbindung_herstellen(self):
        """Verbindung zur Datenbank herstellen"""
        self.verbindung = sqlite3.connect(self.pfad)

        if self.ist_neu:
            self.datenbank_erstellen()

    def datenbank_erstellen(self):
        """Eine passende Datenbank wird erstellt"""
        c = self.verbindung.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS buecher
                     (
                         id       integer
                             constraint id primary key,
                         titel    TEXT,
                         autor    TEXT,
                         lagerort TEXT
                     )""")
        self.verbindung.commit()

    def __del__(self):
        if hasattr(self, "verbindung"):
            self.verbindung.close()


def main():
    """HauptFUNKTION unseres Bibliothekprogramms"""
    f = Figlet(font='slant')
    print(f.renderText('Bibliothek'))

    items = ["Buch suchen", "Buch hinzufügen", "Inventarliste ausgeben", "Programmende"]

    for n, i in enumerate(items, 1):
        print(f"{n}\t{i}")


ordner = Path(__file__).parent  # Ordner wird ermittelt
db_name = ordner / "bibliothek.db"  # Pfad wird erstellt

db = Datenbank(db_name)  # Instanz der Klasse Datenbank wird erstellt, der Datenbankname mit Pfad wird übergeben
meine_bibliothek = Bibliothek(
    db)  # Instanz der Klasse Bibliothek wird erstellt, und die Instanz der Datenbank wird übergeben.

# Buch hinzufügen:
# buch2 = Buch("Brave New World", "Aldous Huxley", "B4-001") # Objekt der Klasse Buch erstellen
# buch3 = Buch("Daten- und Prozessanalyse", "Sascha Kersken", "B10-011") # Objekt der Klasse Buch erstellen
#
# for i in buch2, buch3:
#     meine_bibliothek.buch_hinzufuegen(i)

# Alle Bücher ausgeben:
# meine_bibliothek.alle_bucher_ausgeben()

# Ein Buch suchen:
# meine_bibliothek.buch_suchen("Brave")

if __name__ == "__main__":
    main()



