from cryptography.fernet import Fernet #Fernet ---> daten in db speichern
import mysql.connector
from pathlib import Path

# ------------------------
# Schlüssel laden/erstellen
# ------------------------
KEY_FILE = Path("fernet.key")


def load_or_create_key():
    if KEY_FILE.exists():
        return KEY_FILE.read_bytes()
    else:
        key = Fernet.generate_key()
        KEY_FILE.write_bytes(key)
        return key


key = load_or_create_key()
cipher = Fernet(key)

# ------------------------
# MySQL-Verbindung
# ------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "FCbarcelona2025 !", # achtum
    "database": "benutzer",
    "use_pure": True

}


# ------------------------
# Funktion zum Speichern
# ------------------------
def save_secret_to_db(secret: str) -> int:
    """
    Verschlüsselt den Secret-Text und speichert ihn in der MySQL-Datenbank.
    Gibt die ID des gespeicherten Eintrags zurück.
    """
    encrypted = cipher.encrypt(secret.encode("utf-8"))

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS geheimdaten
                   (
                       id   INT AUTO_INCREMENT PRIMARY KEY,
                       info VARBINARY(500)
                   )
                   """)
    conn.commit()

    cursor.execute("INSERT INTO geheimdaten (info) VALUES (%s)", (encrypted,))
    conn.commit()

    last_id = cursor.lastrowid
    cursor.close()
    conn.close()

    return last_id


# ------------------------
# Funktion zum Abrufen
# ------------------------
def get_secret_from_db(entry_id: int) -> str:
    """
    Liest den verschlüsselten Text aus der DB anhand der ID und entschlüsselt ihn.
    """
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("SELECT info FROM geheimdaten WHERE id=%s", (entry_id,))
    encrypted = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return cipher.decrypt(encrypted).decode("utf-8")


# ------------------------
# Beispielaufruf
# ------------------------
if __name__ == "__main__":
    secret_text = "Mein geheimer API-Key: 12345-ABCDE"

    # Speichern
    secret_id = save_secret_to_db(secret_text)
    print(f"Secret gespeichert mit ID: {secret_id}")

    # Abrufen
    decrypted = get_secret_from_db(secret_id)
    print("Entschlüsselte Nachricht:", decrypted)
