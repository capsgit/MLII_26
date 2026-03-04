from Mitarbeiter import Mitarbeiter

class Angestellter(Mitarbeiter):
    # Angestellter erbt von Mitarbeiter

    def __init__(self, name, gehalt, projektnummer):
      # Aufruf des übergeordneten Konstruktors der Elternklasse mit den Parametern
      super().__init__(name, gehalt)
      self.projektnummer = projektnummer # neues Attribut für die Angestellten Klasse


    def __str__(self):
      return "Ausgabe Angestellte: \nName: " + self.name + " \nGehalt: " + str(self.gehalt) + "\nProjektnummer: " + str(self.projektnummer)

# ENDE der Klassendefinition

# Testobjekt
angestellt = Angestellter("Evelin Müller", 34000, 12345)

# Testlauf der Klasse
print(angestellt)
print("--------ANG--------------")
print(angestellt.zeige_anzahl())