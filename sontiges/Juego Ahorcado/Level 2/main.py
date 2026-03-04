from hm3_lib import zeichne_hangman
from pathlib import Path
from sys import exit
import os
import random
from time import sleep

ordner = Path(__file__).parent
filename = ordner / "palabras_ahorcado"


def spiel_starten():
    gesuchtes_wort = wortauswahl()
    hangman(gesuchtes_wort)


def wort_hinzufuegen():
    """Wörter der Datei hinzufügen"""
    while True:
        neues_wort = input("Bitte geben Sie ein neues Wort ein (Leer lassen, wenn fertig)\n-> ")

        if not neues_wort:
            clear_screen()
            menue()
            break

        elif not neues_wort.isalpha():
            print("Nur Buchstaben eingeben!")
            continue

        else:
            with open(filename, "a", encoding="utf-8") as file:
                file.writelines(neues_wort + "\n")


def woerter_anzeigen():
    """Alle Wörter werden in der Konsole ausgegeben."""
    inhalt = woerter_lesen()
    for n, w in enumerate(inhalt, 1):
        print(f"{n}. {w}", end="")

    print("\nIn 10 Sekunden werden Sie zum Menü zurück geleitet...")
    sleep(10)
    menue()


def wortauswahl():
    woerter = woerter_lesen()
    wort = random.choice(woerter).upper().strip()

    return wort


def woerter_lesen():
    if Path(filename).exists():
        with open(filename, "r", encoding="utf8") as file:
            zeilen = file.readlines()
        return zeilen

    else:
        print("Datei existiert nicht, wird angelegt")
        wort_hinzufuegen()

        return None


def clear_screen():
    """Bildschirm Löschung
    bei Linux oder MAC: clear
    bei Windows cls
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def hangman(gesuchtes_wort):
    fehler = 0
    max_fehler = 6
    geratene_buchstaben = []  # Hier werden später die schon geratenen Buchstaben abgelegt

    while fehler < max_fehler:
        angezeigtes_wort = ""
        for buchstabe in gesuchtes_wort:
            if buchstabe in geratene_buchstaben:
                angezeigtes_wort += buchstabe
            else:
                angezeigtes_wort += "_"

        clear_screen()
        print(zeichne_hangman(fehler))
        print(angezeigtes_wort)
        # print(geratene_buchstaben)  # debugging

        if angezeigtes_wort == gesuchtes_wort:
            print("Gewonnen! Du hast richtig geraten!")
            print("Das gesuchte Wort war: ", gesuchtes_wort)
            print("Du hast", len(geratene_buchstaben) + 1, "Versuche gebraucht.")
            break

        try:
            eingabe = input("Bitte gib einen Buchstaben ein: ").upper()
        except KeyboardInterrupt:
            beenden()

        if not eingabe:
            print("Leere Eingabe nicht erlaubt!")
            sleep(1)

        elif len(eingabe) > 1:
            print("Du darfst nur genau EINEN Buchstaben eingeben!")
            sleep(1)

        elif not eingabe.isalpha():
            print("Bitte nur Buchstaben eingeben!")
            sleep(1)


        elif eingabe in geratene_buchstaben:
            print("Du hast diesen Buchstaben schon geraten!")


        elif eingabe in gesuchtes_wort:
            print("Richtig geraten!")
            geratene_buchstaben.append(eingabe)

        else:
            print("Falsch geraten!")
            fehler += 1
            geratene_buchstaben.append(eingabe)
            sleep(1)

    else:
        print(zeichne_hangman(fehler))
        print("Du hast leider verloren, das gesuchte Wort war:", gesuchtes_wort)
        sleep(5)
        menue()


def beenden():
    """Programm wird ordnungsgemäß beendet."""
    print("Spielende! Bis zum nächsten Mal!")
    exit(0)


def menue():
    auswahl = None
    menu_items = ["Spielen", "Neues Wort hinzufügen", "Wortliste ausgeben", "Spiel beenden"]
    print()
    print("~ Hangman ~")
    for n, i in enumerate(menu_items, 1):  # nummeriere und starte bei 1
        print(f"{n} - {i}")

    try:
        # Optimaler Fall
        auswahl = input("-> ")

    except KeyboardInterrupt:
        # Falls ein Fehler auftritt, mache Folgendes:
        beenden()  # Beenden-Funktion aufrufen

    match auswahl:
        case "1":
            spiel_starten()

        case "2":
            wort_hinzufuegen()

        case "3":
            woerter_anzeigen()

        case "4":
            beenden()

        case _:
            print("Ungültige Auswahl")
            menue()


if __name__ == "__main__":
    menue()
