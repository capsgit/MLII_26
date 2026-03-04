# import random
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from pyfiglet import Figlet

# =========================
# MODELO (datos en memoria)
# =========================
@dataclass
class Libro:
    """
    Representa un libro en Python.
    OJO: en la base de datos además existe un 'id' autogenerado,
    por eso aquí no lo incluimos.
    """
    titulo: str
    autor: str
    editorial: str
    año_de_publicacion: int
    copias: int
    disponibilidad: bool


# =========================
# DB (encapsula la conexión)
# =========================
class Datenbank:
    """
    Clase responsable de:
    - abrir la conexión SQLite
    - crear la tabla si no existe
    - cerrar la conexión al final
    """
    def __init__(self, ruta: Path):
        self.ruta = Path(ruta)
        self.coneccion = sqlite3.connect(self.ruta)

        # Para poder usar row["columna"] en vez de row[0], row[1], ...
        self.coneccion.row_factory = sqlite3.Row

        self.crear_base_datos()

    def crear_base_datos(self):
        """
        Crea la tabla 'libros' si no existe.
        - disponibilidad se guarda como 0/1 (int), pero en Python lo usamos como bool.
        """
        c = self.coneccion.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS libros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                autor TEXT NOT NULL,
                editorial TEXT NOT NULL,
                año_de_publicacion INTEGER NOT NULL,
                copias INTEGER NOT NULL CHECK(copias >= 0),
                disponibilidad INTEGER NOT NULL CHECK(disponibilidad IN (0, 1))
            )
        """)
        self.coneccion.commit()

    def close(self):
        """Cierra la conexión si está abierta."""
        if self.coneccion:
            self.coneccion.close()


# =========================
# LOGICA (CRUD)
# =========================
class Biblioteca:
    """
    Aquí va la lógica de negocio:
    - agregar, listar, buscar, editar, borrar, contar
    """

    # Campos permitidos para UPDATE (evita errores por typos y hace el método más seguro)
    CAMPOS_EDITABLES = {"titulo", "autor", "editorial", "año_de_publicacion", "copias", "disponibilidad"}

    def __init__(self, db: Datenbank):
        self.db = db

    def agregar_libro(self, libro: Libro) -> None:
        """
        Inserta un libro en la DB.
        Usamos placeholders (?) para no concatenar strings y evitar problemas.
        """
        c = self.db.coneccion.cursor()
        c.execute("""
            INSERT INTO libros (titulo, autor, editorial, año_de_publicacion, copias, disponibilidad)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            libro.titulo,
            libro.autor,
            libro.editorial,
            libro.año_de_publicacion,
            libro.copias,
            int(libro.disponibilidad),  # bool -> 0/1
        ))
        self.db.coneccion.commit()

    def mostrar_libros(self) -> None:
        """Muestra todos los libros en formato de tabla."""
        c = self.db.coneccion.cursor()
        c.execute("SELECT * FROM libros ORDER BY id")
        filas = c.fetchall()

        print("\n--------- Lista de libros en la biblioteca ---------")
        if not filas:
            print("(La lista está vacía)")
            return

        print(f'{"ID":<4} {"TÍTULO":<35} {"AUTOR":<25} {"EDITORIAL":<15} {"AÑO":<6} {"COP":<5} {"DISP":<6}')
        print("-" * 90)

        for row in filas:
            disp = "✅" if row["disponibilidad"] == 1 else "❌"
            print(f'{row["id"]:<4} '
                  f'{row["titulo"][:24]:<35} '
                  f'{row["autor"][:19]:<25} '
                  f'{row["editorial"][:14]:<15} '
                  f'{row["año_de_publicacion"]:<6} '
                  f'{row["copias"]:<5} '
                  f'{disp:<6}')

        print("-" * 90)
        print("Total libros en DB:", self.contar_libros())

    def buscar_libro(self, titulo: str) -> None:
        """
        Busca libros cuyo título contenga el texto ingresado.
        LIKE con %texto% => coincidencias parciales.
        """
        c = self.db.coneccion.cursor()
        c.execute("SELECT * FROM libros WHERE titulo LIKE ? ORDER BY id", (f"%{titulo}%",))
        filas = c.fetchall()

        print("\n=============== Resultados ===============")
        if not filas:
            print("(No se encontraron coincidencias)")
            return

        print(f'{"ID":<4} | {"TÍTULO":<25} | {"AUTOR":<20} | {"EDITORIAL":<15} | {"AÑO":<6} | {"COP":<5} | {"DISP":<6}')
        print("-" * 110)

        for row in filas:
            disp = "✅" if row["disponibilidad"] == 1 else "❌"
            print(f'{row["id"]:<4} | {row["titulo"]:<25} | {row["autor"]:<20} | {row["editorial"]:15} | '
                  f'{row["año_de_publicacion"]:<6} | {row["copias"]:<5} | {disp}')

    def borrar_libro_por_id(self, libro_id: int) -> bool:
        """Borra un libro por id. Devuelve True si borró algo."""
        c = self.db.coneccion.cursor()
        c.execute("DELETE FROM libros WHERE id = ?", (libro_id,))
        self.db.coneccion.commit()
        return c.rowcount > 0

    def contar_libros(self) -> int:
        """Cuenta cuántos registros hay en la tabla."""
        c = self.db.coneccion.cursor()
        c.execute("SELECT COUNT(*) AS n FROM libros")
        return c.fetchone()["n"]

    def editar_libro(self, libro_id: int, **kwargs) -> bool:
        """
        Actualiza campos de un libro por id.
        Ej: editar_libro(3, titulo="Nuevo", copias=5)

        kwargs puede traer varios campos a la vez.
        """
        if not kwargs:
            return False

        # Filtramos claves no permitidas
        kwargs = {k: v for k, v in kwargs.items() if k in self.CAMPOS_EDITABLES}
        if not kwargs:
            return False

        campos = []
        valores = []

        for campo, valor in kwargs.items():
            campos.append(f"{campo} = ?")

            # Guardamos disponibilidad como 0/1
            if campo == "disponibilidad":
                valor = int(bool(valor))

            valores.append(valor)

        valores.append(libro_id)

        sql = f"UPDATE libros SET {', '.join(campos)} WHERE id = ?"

        c = self.db.coneccion.cursor()
        c.execute(sql, valores)
        self.db.coneccion.commit()

        return c.rowcount > 0

def terminar():
    print("\n👋 Juego terminado. ¡Hasta luego!")
    exit(0)

'''
# =========================
# SEED
# =========================
def seed_libros(biblio: Biblioteca, n: int = 60) -> None:
    """
    Llena la base de datos con libros de prueba.
    Si ya existen libros, no vuelve a insertarlos.
    """

    # 1) Evitar duplicados creando un índice único lógico
    c = biblio.db.coneccion.cursor()
    c.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS ux_libro_unico
        ON libros(titulo, autor, año_de_publicacion)
    """)
    biblio.db.coneccion.commit()

    # 2) Datos base
    titulos = [
        # Latinoamérica
        "Cien años de soledad", "El amor en los tiempos del cólera", "Crónica de una muerte anunciada",
        "La casa de los espíritus", "Eva Luna", "Pedro Páramo", "Rayuela", "Los detectives salvajes",
        "2666", "La ciudad y los perros", "Conversación en La Catedral", "La fiesta del Chivo",
        "El túnel", "Sobre héroes y tumbas", "Ensayo sobre la ceguera", "El evangelio según Jesucristo",
        "La tregua", "El astillero",

        # Clásicos universales
        "1984", "Rebelión en la granja", "Fahrenheit 451", "Un mundo feliz",
        "El nombre de la rosa", "El péndulo de Foucault", "La sombra del viento",
        "El juego del ángel", "El prisionero del cielo",
        "El retrato de Dorian Gray", "Drácula", "Frankenstein",
        "Crimen y castigo", "Los hermanos Karamázov", "Guerra y paz", "Anna Karénina",
        "Madame Bovary", "El conde de Montecristo", "Los trevs mosqueteros",
        "Moby Dick", "El viejo y el mar", "Las aventuras de Tom Sawyer",

        # Literatura moderna
        "Tokio Blues", "Kafka en la orilla", "1Q84", "Siddhartha", "Demian",
        "El lobo estepario", "El guardián entre el centeno", "En el camino",
        "La insoportable levedad del ser", "La náusea",
        "El extranjero", "La peste", "El proceso", "La metamorfosis",

        # Fantasía / Sci-Fi
        "Dune", "Neuromante", "Fundación", "Yo, Robot",
        "El señor de los anillos", "El hobbit",
        "Juego de tronos", "Choque de reyes", "Tormenta de espadas",
        "Harry Potter y la piedra filosofal", "Harry Potter y la cámara secreta"
    ]

    autores = [
        # Latinoamérica
        "Gabriel García Márquez", "Isabel Allende", "Juan Rulfo", "Julio Cortázar",
        "Roberto Bolaño", "Mario Vargas Llosa", "Ernesto Sábato", "José Saramago",
        "Mario Benedetti",

        # Clásicos
        "George Orwell", "Ray Bradbury", "Aldous Huxley", "Umberto Eco",
        "Carlos Ruiz Zafón", "Oscar Wilde", "Bram Stoker", "Mary Shelley",
        "Fiódor Dostoyevski", "León Tolstói", "Gustave Flaubert",
        "Alexandre Dumas", "Herman Melville", "Mark Twain",

        # Modernos
        "Haruki Murakami", "Hermann Hesse", "J.D. Salinger", "Jack Kerouac",
        "Milan Kundera", "Jean-Paul Sartre", "Albert Camus", "Franz Kafka",

        # Fantasía / Sci-Fi
        "Frank Herbert", "William Gibson", "Isaac Asimov",
        "J.R.R. Tolkien", "George R.R. Martin", "J.K. Rowling"
    ]

    editoriales = [
        "Sudamericana", "Secker & Warburg", "Bompiani", "Minotauro",
        "Planeta", "Alfaguara", "Anagrama", "Random House"
    ]

    # 3) Generación de libros
    filas = []

    for _ in range(n):
        titulo = random.choice(titulos)
        autor = random.choice(autores)
        editorial = random.choice(editoriales)
        año = random.randint(1940, 2024)
        copias = random.randint(0, 10)
        disponibilidad = 1 if copias > 0 else 0

        filas.append((titulo, autor, editorial, año, copias, disponibilidad))

    # 4) Inserción masiva evitando duplicados
    c.executemany("""
        INSERT OR IGNORE INTO libros
        (titulo, autor, editorial, año_de_publicacion, copias, disponibilidad)
        VALUES (?, ?, ?, ?, ?, ?)
    """, filas)

    biblio.db.coneccion.commit()

    print(f"✅ Seed ejecutada. Libros en DB: {biblio.contar_libros()}")
'''

# =========================
# HELPERS DE INPUT
# =========================
def input_int(msg: str, min_val: int | None = None) -> int:
    """Pide un int hasta que el usuario lo ingrese bien."""
    while True:
        raw = input(msg).strip()
        try:
            val = int(raw)
            if min_val is not None and val < min_val:
                print(f"❌ Debe ser >= {min_val}")
                continue
            return val
        except ValueError:
            print("❌ Ingresa un número válido.")

def input_bool(msg: str) -> bool:
    """Convierte respuesta humana a bool."""
    while True:
        raw = input(msg + " (s/n): ").strip().lower()
        if raw in {"s", "si", "sí", "y", "yes", "1", "true", "t"}:
            return True
        if raw in {"n", "no", "0", "false", "f"}:
            return False
        print("❌ Responde con s/n.")

def pedir_libro_por_input() -> Libro:
    """Construye un Libro a partir de inputs."""
    titulo = input("Título: ").strip()
    autor = input("Autor: ").strip()
    editorial = input("Editorial: ").strip()
    año = input_int("Año de publicación: ", min_val=0)
    copias = input_int("Copias: ", min_val=0)
    disponibilidad = input_bool("¿Disponible?")
    return Libro(titulo, autor, editorial, año, copias, disponibilidad)

def pausa():
    input("\nPulsa Enter para continuar...")


# =========================
# MENU PRINCIPAL
# =========================
def main():
    f = Figlet(font="pagga")

    ordner = Path(__file__).parent
    db_path = ordner / "bibliothek.db"

    db = Datenbank(db_path)
    biblio = Biblioteca(db)
    # seed_libros(biblio)
    try:
        while True:
            print("\n========================================")
            print(f.renderText("Biblioteca"))
            print("========================================")
            print("1) Ver lista de libros")
            print("2) Buscar por título")
            print("3) Agregar libro")
            print("4) Editar libro")
            print("5) Borrar libro por ID")
            print("0) Salir")

            op = input("Elige: ").strip()

            if op == "1":
                biblio.mostrar_libros()
                pausa()

            elif op == "2":
                q = input("Título a buscar: ").strip()
                biblio.buscar_libro(q)
                pausa()

            elif op == "3":
                libro = pedir_libro_por_input()
                biblio.agregar_libro(libro)
                print("✅ Libro agregado.")
                pausa()

            elif op == "4":
                libro_id = input_int("ID del libro a editar: ", min_val=1)
                print("Deja vacío si no quieres cambiar un campo.\n")

                nuevo_titulo = input("Nuevo título: ").strip()
                nuevo_autor = input("Nuevo autor: ").strip()
                nueva_editorial = input("Nueva editorial: ").strip()

                cambios = {}

                if nuevo_titulo:
                    cambios["titulo"] = nuevo_titulo
                if nuevo_autor:
                    cambios["autor"] = nuevo_autor
                if nueva_editorial:
                    cambios["editorial"] = nueva_editorial

                # Año/copies: pedimos y validamos SOLO si el usuario escribió algo
                año_raw = input("Nuevo año de publicación: ").strip()
                if año_raw:
                    # validación simple
                    try:
                        cambios["año_de_publicacion"] = int(año_raw)
                    except ValueError:
                        print("❌ Año inválido. (no se actualiza año)")

                copias_raw = input("Nuevas copias: ").strip()
                if copias_raw:
                    try:
                        cambios["copias"] = int(copias_raw)
                    except ValueError:
                        print("❌ Copias inválidas. (no se actualiza copias)")

                disp_raw = input("¿Disponible? (s/n, vacío=no cambiar): ").strip().lower()
                if disp_raw in ("s", "si", "sí", "y", "1", "true"):
                    cambios["disponibilidad"] = True
                elif disp_raw in ("n", "no", "0", "false"):
                    cambios["disponibilidad"] = False

                if not cambios:
                    print("No se ingresaron cambios.")
                else:
                    ok = biblio.editar_libro(libro_id, **cambios)
                    print("✅ Libro actualizado." if ok else "❌ No se encontró el ID.")

                pausa()

            elif op == "5":
                libro_id = input_int("ID a borrar: ", min_val=1)
                ok = biblio.borrar_libro_por_id(libro_id)
                print("✅ Borrado." if ok else "❌ No existe ese ID.")
                pausa()

            elif op == "0":
                print("👋 Chao.")
                break

            else:
                print("❌ Opción inválida.")
                pausa()

    finally:
        db.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        terminar()
