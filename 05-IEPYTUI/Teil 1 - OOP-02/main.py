#empieza
from Angestellter import Angestellter, angestellt

# Objekte erstellen
angest1 = Angestellter("Zara Svennson", 20000, 3456)
angest2 = Angestellter("Manni Deutsch", 50000, 678)

# Ausführen verschiedener Methoden
print(angest1)
print("===============")
print(angest2)

angest2.gehalt = 44300
print(angest2)

print(angestellt.zeige_anzahl())