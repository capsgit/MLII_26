import mysql.connector as mc
from mysql.connector import Error

config = {
    "host": "localhost",      # mejor que "localhost" a veces
    "user": "root",
    "password": "FCbarcelona2025 !",
    "database": "Warenkataloge",
    "use_pure": True,
}

DB_NAME = "warenkataloge"

neue_eintraege = [
    ("Jabon", "AS0123", 7.50),
    ("Papel", "AS0980", 6.25),
    ("Auto BMW",  "AU0171", 1500.00),
    ("Toalla",  "AS0172", 5.00),
]

# Verbindung herstellen:
try:
    conn = mc.connect(**config)
    print("✅ Conectado a MySQL:", conn.get_server_info())

    c = conn.cursor()

    # 1) Crear DB si no existe
    c.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    c.execute(f"USE {DB_NAME}")

    # (Opcional) asegurar tabla existe (evita dudas)
    c.execute("""
    CREATE TABLE IF NOT EXISTS inventario (
        id INT PRIMARY KEY AUTO_INCREMENT,
        produkt_name VARCHAR(100) NOT NULL,
        artikelnummer VARCHAR(50) UNIQUE NOT NULL,
        netto_preis DECIMAL(10,2) NOT NULL
    )
    """)

    # 3) Insertar

    sql = """
    INSERT INTO inventario (produkt_name, artikelnummer, netto_preis)
    VALUES (%s, %s, %s) AS new
    ON DUPLICATE KEY UPDATE
        produkt_name = new.produkt_name,
        netto_preis  = new.netto_preis
    """

    c.executemany(sql, neue_eintraege)

    conn.commit()
    print(f"✅ Insertados: {c.rowcount}")

except Error as e:
    print("❌ MySQL Error:", e)

finally:
    if conn and conn.is_connected():
        conn.close()
        print("🔌 Conexión cerrada.")