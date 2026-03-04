from hm3_lib import zeichne_hangman  # debe ser función
import random
import os
from pathlib import Path
from sys import exit
from time import sleep

DB = Path(__file__).parent / "palabras_ahorcado.txt"

# =========================
# PERSISTENCIA (DB)
# =========================

def cargar_palabras():
    """Devuelve una lista de palabras desde el archivo. Si no existe, lo crea."""
    if not DB.exists():
        DB.touch()  # crea el archivo vacío
        return []

    with open(DB, "r", encoding="utf-8") as f:
        palabras = [x.strip().lower() for x in f if x.strip()]

    # opcional: quitar duplicados manteniendo orden
    palabras_unicas = list(dict.fromkeys(palabras))
    return palabras_unicas

def agregar_palabra_archivo(palabra: str):
    """Agrega una palabra al archivo (append)."""
    with open(DB, "a", encoding="utf-8") as f:
        f.write(palabra + "\n")


# =========================
# UTILIDAD UI
# =========================

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def mostrar_vidas(vidas, max_vidas):
    """
    Devuelve un string con corazones rojos (vidas actuales)
    y grises/negros (vidas perdidas)
    """
    return "❤️" * vidas + "🖤" * (max_vidas - vidas)


# =========================
# MENÚ
# =========================

def mostrar_menu():
    print("\n=== AHORCADO ===")
    print("1. Jugar")
    print("2. Mirar la lista de posibles palabras")
    print("3. Incluir palabras a la lista")
    print("4. Terminar / Cerrar")
    return input("Elige una opción (1-4): ").strip()

def mostrar_palabras(palabras):
    print("\n--- Lista de palabras ---")
    if not palabras:
        print("(La lista está vacía)")
        return
    for i, p in enumerate(palabras, start=1):
        print(f"{i}. {p}")

def pedir_palabra_nueva():
    palabra = input("Escribe una palabra para agregar: ").strip().lower()
    if not palabra:
        print("❌ No puedes agregar una palabra vacía.")
        return None
    if not palabra.isalpha():
        print("❌ Solo se permiten letras (sin espacios ni números).")
        return None
    return palabra


# =========================
# LÓGICA DE JUEGO
# =========================

def mostrar_progreso(palabra, acertadas):
    return " ".join([letra if letra in acertadas else "_" for letra in palabra])

def palabra_completa(palabra, acertadas):
    return all(letra in acertadas for letra in palabra)

def pedir_intento():
    intento = input("Ingresa una letra o intenta la palabra completa: ").strip().lower()
    if not intento:
        print("❌ Entrada vacía.")
        return None
    if not intento.isalpha():
        print("❌ Solo se permiten letras (sin espacios ni números).")
        return None
    return intento

def jugar(palabras):
    if not palabras:
        print("⚠️ No hay palabras. Agrega algunas primero (opción 3).")
        return

    palabra = random.choice(palabras)
    MAX_VIDAS = 6
    vidas = MAX_VIDAS
    acertadas = set()
    falladas = set()
    intentos_palabra = set()

    while vidas > 0 and not palabra_completa(palabra, acertadas):
        fallos = 6 - vidas  # para el dibujo
        clear_screen()
        print(zeichne_hangman(fallos))
        print("\nPalabra:", mostrar_progreso(palabra, acertadas))
        print("Fallos :", " ".join(sorted(falladas)) if falladas else "(ninguno)")
        print("Vidas  :", mostrar_vidas(vidas, MAX_VIDAS))

        intento = pedir_intento()
        if intento is None:
            continue

        if len(intento) == 1:
            letra = intento
            if letra in acertadas or letra in falladas:
                print("ℹ️ Ya intentaste esa letra.")
                input("Enter para continuar...")
                continue

            if letra in palabra:
                acertadas.add(letra)
                print("✅ ¡Bien! La letra está.")
            else:
                falladas.add(letra)
                vidas -= 1
                print("❌ No está. Pierdes una vida.")
            input("Enter para continuar...")

        else:
            if intento in intentos_palabra:
                print("ℹ️ Ya intentaste esa palabra completa.")
                input("Enter para continuar...")
                continue

            intentos_palabra.add(intento)

            if intento == palabra:
                acertadas.update(set(palabra))
                print("🎉 ¡Correcto! Adivinaste la palabra completa.")
            else:
                vidas -= 1
                print("❌ No es la palabra. Pierdes una vida.")
            input("Enter para continuar...")

    clear_screen()
    print(zeichne_hangman(6 - vidas))
    if palabra_completa(palabra, acertadas):
        print("\n🏆 ¡Ganaste! La palabra era:", palabra)
    else:
        print("\n💀 Perdiste. La palabra era:", palabra)

def terminar():
    print("\n👋 Juego terminado. ¡Hasta luego!")
    exit(0)


# =========================
# PROGRAMA PRINCIPAL
# =========================

def main():
    palabras = cargar_palabras()

    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            jugar(palabras)

        elif opcion == "2":
            mostrar_palabras(palabras)
            sleep(3)

        elif opcion == "3":
            nueva = pedir_palabra_nueva()
            if nueva:
                if nueva in palabras:
                    print("ℹ️ Esa palabra ya está en la lista.")
                else:
                    palabras.append(nueva)           # actualiza memoria
                    agregar_palabra_archivo(nueva)   # persiste en archivo
                    print("✅ Palabra agregada y guardada.")
            sleep(3)

        elif opcion == "4":
            terminar()

        else:
            print("❌ Opción inválida.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        terminar()
