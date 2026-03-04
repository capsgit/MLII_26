# *-* coding: utf-8 *-*

import sqlite3
import sys
import os
from pathlib import Path
import pyfiglet
import logging

HERE = Path(__file__).resolve()
ROOT_DIR = next(p for p in HERE.parents if (p / "druckst_du.py").exists())

sys.path.insert(0, str(ROOT_DIR))  # insert(0) > append, tiene prioridad

from druckst_du import wait_for_keypress


demo_entries = [
    ("Max", "Mustermann", 49, 1701234567),
    ("Erika", "Musterfrau", 49, 1702345678),
    ("John", "Doe", 1, 2125551234),
    ("Jane", "Smith", 1, 2125555678),
    ("Hans", "Schmidt", 49, 1703456789),
    ("Clara", "Schneider", 49, 1704567890),
    ("Michael", "Müller", 49, 1705678901),
    ("Sarah", "Meier", 49, 1706789012),
    ("David", "Weber", 49, 1707890123),
    ("Anna", "Bauer", 49, 1708901234),
    ("Tom", "Richter", 49, 1709012345),
    ("Linda", "Koch", 49, 1700123456),
    ("Paul", "Schulz", 49, 1701231234),
    ("Laura", "Zimmermann", 49, 1702342345),
    ("Peter", "Hoffmann", 49, 1703453456),
    ("Julia", "Lang", 49, 1704564567),
    ("Alex", "Schwarz", 49, 1705675678),
    ("Eva", "Fischer", 49, 1706786789),
    ("Leon", "Klein", 49, 1707897890),
    ("Sophie", "Wolf", 49, 1708908901)
]



def cls() -> None:
    os.system('cls' if os.name=='nt' else 'clear')


def create_table() -> None:
    query = """CREATE TABLE IF NOT EXISTS telefonbuch (
        id INTEGER PRIMARY KEY,
        firstname TEXT,
        lastname TEXT,
        phone_prefix INTEGER,
        phone_number INTEGER
    )"""

    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute(query)


def print_entries(entries) -> None:
    if len(entries) == 0:
        print('Es wurde kein Eintrag zu Ihrer Suche gefunden.')
    elif len(entries) == 1:
        print('Es wurde ein Eintrag zu Ihrer Suche gefunden.')
    else:
        print(f'Es wurden {len(entries)} Einträge in der Tabelle gefunden.')

    print(f'{'ID':<5}| {'Vorname':<15}| {'Nachname':<15}| {'Vorwahl':<8}| {'Telefonnummer':<15}')
    print('-' * 70)
    for entry in entries:
        db_id, firstname, lastname, phone_prefix, phone_number = entry
        print(f'{db_id:<5}| {firstname[:14]:<15}| {lastname[:14]:<15}| {phone_prefix:<8}| {phone_number:<15}')

    print()


def find_entry() -> None:
    search_term = input("Suchbegriff: ")
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM telefonbuch WHERE firstname LIKE ?", (f"%{search_term}%",))
        entries = cursor.fetchall()

    print_entries(entries)

    wait_for_keypress()
    cls()
    menu()


def add_entry() -> None:
    firstname = input("Vorname: ")
    lastname = input("Nachname: ")
    phone_prefix = input("Vorwahl: ")
    phone_number = input("Telefonnummer: ")

    if not firstname or not lastname or not phone_prefix or not phone_number:
        print('Bitte geben Sie alle Felder an.')
        add_entry()

    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO telefonbuch (firstname, lastname, phone_prefix, phone_number) VALUES (?, ?, ?, ?)", (firstname, lastname, phone_prefix, phone_number))
        conn.commit()

    msg = f'Der Eintrag wurde der Tabelle erfolgreich hinzugefügt: {firstname} {lastname}'
    logger.debug(msg)
    print(f'\n{msg}')
    print()
    wait_for_keypress()
    cls()
    menu()


def remove_entry() -> None:
    view_entries(False)

    while True:
        entry = input('Welcher Datensatz soll gelöscht werden? ')
        if entry.isdigit():
            entry = int(entry)
            break
        else:
            print('Bitte eine gültige Zahl eingeben')

    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM telefonbuch WHERE id=?', (entry,))
        result = cursor.fetchone()

        if result:
            cursor.execute("DELETE FROM telefonbuch WHERE id=?", (entry,))
            conn.commit()
            msg = f'Der Eintrag mit der ID: {entry} wurde gelöscht'
            logger.debug(msg)
            print(msg)
        else:
            msg = f'Der Eintrag mit der ID: {entry} konnte nicht gefunden werden.'
            logger.debug(msg)
            print(msg)

    wait_for_keypress()
    cls()
    menu()


def view_entries(wait: bool = True):
    print()
    print(f'Folgende Einträge sind in der Tabelle enthalten:')
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM telefonbuch")
        entries = cursor.fetchall()

        print_entries(entries)

    if wait:
        wait_for_keypress()
        cls()
        menu()


def exit_program():
    print("\nProgramm beendet.")
    sys.exit()


def get_max_len_in_menu(items) -> int:
    max_len = 0
    for item in items:
        max_len = max(max_len, len(item))
    return max_len


def add_demo_entries():
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        for entry in demo_entries:
            cursor.execute("INSERT INTO telefonbuch (firstname, lastname, phone_prefix, phone_number) VALUES (?, ?, ?, ?)", entry)
            conn.commit()

    print('Demo Daten wurden der Tabelle hinzugefügt')
    wait_for_keypress()
    cls()
    menu()


def menu() -> None:
    items = ['Eintrag suchen', 'Eintrag hinzufügen', 'Eintrag löschen', 'Alle Einträge anzeigen', 'Demo Daten einfügen', 'Beenden']
    max_len = get_max_len_in_menu(items)

    try:
        print(pyfiglet.figlet_format("Telefonbuch"))
        print('#' * int(max_len + 7))
        print(f'#{'Menü':^{max_len+5}}#')
        print('-' * int(max_len + 7))
        print(f'#{'':^{max_len + 5}}#')

        for idx, item in enumerate(items):
            text = f'# {idx+1}: {item}'
            print(f'{text:<{max_len+5}} #')

        print(f'#{'':^{max_len + 5}}#')
        print('#' * int(max_len + 7))

        selection = input('\nWas möchten Sie tun?: ')

        match selection:
            case '1':
                find_entry()
            case '2':
                add_entry()
            case '3':
                remove_entry()
            case '4':
                view_entries()
            case '5':
                add_demo_entries()
            case '6':
                exit_program()

    except KeyboardInterrupt:
        exit_program()


if __name__ == "__main__":
    folder = Path(__file__).parent
    database = folder / "telefonbuch.db"
    logging.basicConfig(
        level=logging.DEBUG,
        filename='logfile.log',
        encoding='utf-8',
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    create_table()
    menu()