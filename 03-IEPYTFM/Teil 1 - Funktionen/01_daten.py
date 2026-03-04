import csv

daten = [
    ['Name', 'Alter', 'Beruf'],
    ['Max', 29, 'Ingenieur'],
    ['Sophie', 22, 'Lehrerin'],
    ['Tom', 35, 'Entwickler']
]

# escribe esto en un CSV-file
with open('daten.csv', 'w', newline='', encoding="utf-8") as csvfile: # abrir file
    writer = csv.writer(csvfile) # se crea un writer (necesario)
    writer.writerows(daten)

print("Datei erstellt.")