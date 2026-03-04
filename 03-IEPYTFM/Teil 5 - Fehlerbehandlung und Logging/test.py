"""import logging
from logging.handlers import RotatingFileHandler

# Logger erstellen
logger = logging.getLogger('MeinLogger')
logger.setLevel(logging.DEBUG)

# RotatingFileHandler erstellen
handler = RotatingFileHandler('mein_log.log', maxBytes=10000, backupCount=5, delay=True)

# Formatter erstellen und dem Handler hinzufügen
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Handler zum Logger hinzufügen
logger.addHandler(handler)

# Testnachrichten loggen
for i in range(1000):
    logger.debug('Dies ist eine Debug-Nachricht %d', i)"""


import math

def pedir_numero(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Entrada inválida. Ingresa un número.")

def dividir():
    while True:
        try:
            dividendo = pedir_numero("Ingresa un numero a dividir: ")
            divisor   = pedir_numero("Ingresa el numero divisor: ")

            resultado = dividendo / divisor
            print("Resultado:", resultado)
            break   # sale del loop si todo salió bien

        except ZeroDivisionError:
            print("No se puede dividir entre 0. Intenta nuevamente.")

    print("Fin del programa")

dividir()
