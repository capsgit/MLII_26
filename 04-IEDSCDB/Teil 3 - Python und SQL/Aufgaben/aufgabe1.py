import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "FCbarcelona2025 !",
    "database": "warenkataloge",
    "port": 3306
}

TABLE = "inventario"

def create_connection():
    """Crea y devuelve una conexión MySQL."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"❌ Error conectando a MySQL: {e}")
        return None


# -------------------------
# 1) Produktliste anzeigen
# -------------------------
def list_products():
    conn = create_connection()
    if not conn:
        return

    sql = f"""
        SELECT id, produkt_name,  artikelnummer, netto_preis, stock, ort
        FROM {TABLE}
        ORDER BY id
    """

    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        if not rows:
            print("ℹ️ No hay productos.")
            return

        # impresión simple tipo tabla
        headers = ["id", "produkt_name", "artikelnummer", "netto_preis", "stock", "ort"]
        widths = [max(len(str(x)) for x in [h] + [r[i] for r in rows]) for i, h in enumerate(headers)]

        def fmt_row(r):
            return " | ".join(str(r[i]).ljust(widths[i]) for i in range(len(headers)))

        print(fmt_row(headers))
        print("-+-".join("-" * w for w in widths))
        for r in rows:
            print(fmt_row(r))

    except Error as e:
        print(f"❌ Error listando productos: {e}")
    finally:
        cur.close()
        conn.close()


# -------------------------
# 2) Produktdaten aktualisieren nach ID
# -------------------------
def update_product_by_id(product_id: int, **fields):
    """
    Actualiza campos del producto por id.
    Ej: update_product_by_id(3, name="Mouse", preis=19.99)
    """
    if not fields:
        print("ℹ️ No pasaste campos para actualizar.")
        return

    allowed = {"artikelnummer", "name", "preis", "kategorie", "stock", "ort"}
    fields = {k: v for k, v in fields.items() if k in allowed}

    if not fields:
        print("ℹ️ Ningún campo permitido para actualizar.")
        return

    set_clause = ", ".join([f"{k}=%s" for k in fields.keys()])
    values = list(fields.values()) + [product_id]

    sql = f"UPDATE {TABLE} SET {set_clause} WHERE id=%s"

    conn = create_connection()
    if not conn:
        return

    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()

        if cur.rowcount == 0:
            print(f"⚠️ No existe producto con id={product_id} (nada actualizado).")
        else:
            print(f"✅ Producto id={product_id} actualizado.")
    except Error as e:
        print(f"❌ Error actualizando producto: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


# -------------------------
# 3) Produkt löschen (por ID)
# -------------------------
def delete_product_by_id(product_id: int):
    conn = create_connection()
    if not conn:
        return

    sql = f"DELETE FROM {TABLE} WHERE id=%s"

    try:
        cur = conn.cursor()
        cur.execute(sql, (product_id,))
        conn.commit()

        if cur.rowcount == 0:
            print(f"⚠️ No existe producto con id={product_id} (nada borrado).")
        else:
            print(f"🗑️ Producto id={product_id} borrado.")
    except Error as e:
        print(f"❌ Error borrando producto: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


# -------------------------
# CLI simple
# -------------------------
def menu():
    while True:
        print("\nWarenkatalog")
        print("1 - Produktliste anzeigen")
        print("2 - Produkt aktualisieren (nach ID)")
        print("3 - Produkt löschen (nach ID)")
        print("e - Ende")

        choice = input("Auswahl: ").strip().lower()

        if choice == "1":
            list_products()

        elif choice == "2":
            try:
                pid = int(input("Produkt-ID: ").strip())
            except ValueError:
                print("❌ ID inválida.")
                continue

            # ejemplo: preguntas campos opcionales
            name = input("Neuer Name (enter para saltar): ").strip()
            preis_txt = input("Neuer Preis (enter para saltar): ").strip()
            kategorie = input("Neue Kategorie (enter para saltar): ").strip()

            fields = {}
            if name:
                fields["name"] = name
            if preis_txt:
                try:
                    fields["preis"] = float(preis_txt.replace(",", "."))
                except ValueError:
                    print("❌ Precio inválido (no actualizo precio).")
            if kategorie:
                fields["kategorie"] = kategorie

            update_product_by_id(pid, **fields)

        elif choice == "3":
            try:
                pid = int(input("Produkt-ID: ").strip())
            except ValueError:
                print("❌ ID inválida.")
                continue
            delete_product_by_id(pid)

        elif choice == "e":
            break
        else:
            print("❌ Opción inválida.")


if __name__ == "__main__":
    menu()
