class Mitarbeiter():
    # BasisKlasse für alle Angestellten Klassn

    anzahl = 0
    def __init__(self, name, gehalt):
        self.name = name
        self.gehalt = gehalt
        Mitarbeiter.anzahl += 1

    @staticmethod # statische Methode - ähnlich wie Klassenattribute ohne Objektverweis aufrufbar
    def zeige_anzahl():
        return "Gesamt Mitarbeiter %d" % Mitarbeiter.anzahl

    def __str__(self):
        return "Name: " + self.name + " \nGehalt: " + str(self.gehalt)

# ENDE der Klassendefinition

# Testobjekt
chef = Mitarbeiter("Markus Boss", 120000)

# Testlauf der Klasse
print("--------CHEF---------------------")
print(chef)
print("--------mitarbeiter---------------------")
print(Mitarbeiter.zeige_anzahl())