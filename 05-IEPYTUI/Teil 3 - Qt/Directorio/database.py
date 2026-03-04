import sqlite3

class Database:
    def __init__(self, dateiname):
        self.dateiname = dateiname
        self.conn = sqlite3.connect(dateiname)
        self.cursor = self.conn.cursor()

    def verbingung_schliessen(self):
       print("Verbindung zu Datenbank geschlossen.")
       self.conn.close()

    def eintrag_suchen(self, suchbegriff):
        self.cursor.execute("SELECT * FROM telefonbuch WHERE nachname LIKE ?", ("%" + suchbegriff + "%",))
        return self.cursor.fetchall()

    def eintrag_hinzufuegen(self, vorname, nachname, vorwahl, rufnummer):
        self.cursor.execute("INSERT INTO telefonbuch (vorname, nachname, vorwahl, rufnummer)VALUES (?, ?, ?, ?)",
                            (vorname, nachname, vorwahl, rufnummer))
        self.conn.commit()

if __name__ == "__main__":
    db = Database("directorio.db")
#    print(db.eintrag_suchen("Müller"))