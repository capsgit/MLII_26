"""from sys import exit

while True:
    zahl = input("Bitte gib eine Zahl ein (e für exit): ")
    teiler = int("bitte geben Sie einen Teiler ein")

    if zahl == "e":
        exit(0)

    try:
        zahl = int(zahl)
        teiler = int(teiler)

        ergebnis = zahl / teiler
        print(f"Das Ergebnis von {zahl} / {teiler} ist {ergebnis}.")

    except ValueError:
        print("Bitte nur Zahlen eingeben!")
        exit(1)

    except ZeroDivisionError:
        print("Der Teiler darf nicht 0 sein!")
        exit(2)"""


"""class InvalidMailError(Exception):
    pass

def mailform(adresse, betreff, inhalt):
    if not "@" in adresse:
        raise InvalidMailError("Diese Adresse scheint keine Mailadresse zu sein.")

    print("empfänger: ", adresse)
    print("betreff: ", betreff)
    print("inhalt: ", inhalt)

    return "Eine Mail wurde versendet."

print(mailform("xxxx@xxxxx", "Test", "Hallo Welt!"))"""
# -------------------------------------------------------------------------
"""
def main():
    logging.debug("Debug-Information")
    logging.info("Allgemeine Info")
    logging.warning("Warnung")
    logging.error("Ein Fehler ist aufgetreten")
    logging.critical("Kritischer Fehler")

if __name__ == "__main__":
    main()"""


#------------------------------------------------------------------------------------------------

import logging.config, logging, requests, json

#requests es un postman
#json para guardar

#vorbeteitung zu logging

logging.config.fileConfig("logging_config.ini")
logger = logging.getLogger("__name__")


def fetch_data(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        logger.info("Daten erfolgreich von %s abgerufen", url)
        data = response.json()

        # mostrar el contenido
        print(json.dumps(data, indent=4, ensure_ascii=False))
        logger.debug(f"Empfangende Daten: {json.dumps(data)}")

        return data

    except requests.exceptions.RequestException as e:
        logger.error("Fehler beim Abrufen der Daten: %s", e)
        return {}

fetch_data("https://httpbin.org/get")


