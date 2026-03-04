# -*- coding: utf-8 -*-
import string
import random
import pyperclip as pc  # muss vorher installiert werden (pip install pyperclip)
from copy import deepcopy, copy

# Zeichenpool erstellen:
kleinbuchstaben = string.ascii_lowercase
grossbuchstaben = string.ascii_uppercase
zeichen = string.punctuation
zahlen = string.digits

# Alle Strings zusammenführen:
zeichenpool = kleinbuchstaben + grossbuchstaben + zeichen + zahlen

laenge = int(input("Wie viele Stellen soll ihr Passwort lang sein? "))

# Zufällige Zeichen aus dem Zeichenpool in eine Liste speichern und in einem String konvertieren:
passwort  = "".join(random.sample(zeichenpool, laenge))

print(passwort)  # Ausgabe PW
pc.copy(passwort)  # PW wird in Zwischenablage kopiert
print("Das Passwort wurde in die Zwischenablage kopiert!")  # yay!

liste1 = [[1, 2], [3, 4]]
liste2 = copy(liste1)

print("1", id(liste1))
print(id(liste2))

print(id(liste1[0]))
print(id(liste2[0]))
