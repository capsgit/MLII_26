import random  # Para elegir una palabra al azar

# =========================
# FUNCIONES DE MENÚ
# =========================

def mostrar_menu():
    """
    Muestra el menú principal y devuelve la opción elegida por el usuario.
    """
    print("\n=== AHORCADO ===")
    print("1. Jugar")
    print("2. Mirar la lista de posibles palabras")
    print("3. Incluir palabras a la lista")
    print("4. Terminar / Cerrar")

    # strip() elimina espacios al principio/final por si el usuario escribe " 1 "
    return input("Elige una opción (1-4): ").strip()

def mostrar_palabras(palabras):
    """
    Imprime la lista actual de palabras disponibles para jugar.
    """
    print("\n--- Lista de palabras ---")
    if not palabras:
        # Si la lista está vacía, avisamos y salimos
        print("(La lista está vacía)")
        return

    # enumerate nos da (índice, palabra). start=1 para que empiece en 1 y no en 0.
    for i, p in enumerate(palabras, start=1):
        print(f"{i}. {p}")

def pedir_palabra_nueva():
    """
    Pide al usuario una palabra y la valida.
    Devuelve la palabra (en minúscula) o None si es inválida.
    """
    palabra = input("Escribe una palabra para agregar: ").strip().lower()

    # Validación 1: no permitir vacío
    if not palabra:
        print("❌ No puedes agregar una palabra vacía.")
        return None

    # Validación 2: solo letras (sin espacios, números o símbolos)
    if not palabra.isalpha():
        print("❌ Solo se permiten letras (sin espacios ni números).")
        return None

    return palabra


# =========================
# FUNCIONES DE JUEGO
# =========================

def mostrar_progreso(palabra, acertadas):
    """
    Construye cómo se ve la palabra en pantalla.
    Ej: palabra='python', acertadas={'p','o'} -> 'p _ _ _ o _'
    """
    # Recorremos cada letra y mostramos la letra si fue acertada, si no "_"
    return " ".join([letra if letra in acertadas else "_" for letra in palabra])


def palabra_completa(palabra, acertadas):
    """
    Devuelve True si TODAS las letras de la palabra están en 'acertadas'.
    """
    # all(...) devuelve True si todas las condiciones son True
    return all(letra in acertadas for letra in palabra)


def pedir_intento():
    """
    Pide al usuario un intento:
    - Puede ser 1 letra (intento de letra)
    - O una palabra completa (intento de resolver)
    Devuelve el string validado o None si es inválido.
    """
    intento = input("Ingresa una letra o intenta la palabra completa: ").strip().lower()

    # Si está vacío, es inválido
    if not intento:
        print("❌ Entrada vacía.")
        return None

    # Solo letras (nada de espacios, números, etc.)
    if not intento.isalpha():
        print("❌ Solo se permiten letras (sin espacios ni números).")
        return None

    return intento


def jugar(palabras):
    """
    Ejecuta UNA partida del juego del ahorcado.
    """
    # Si no hay palabras, no podemos jugar
    if not palabras:
        print("⚠️ No hay palabras en la lista. Agrega algunas primero (opción 3).")
        return

    # 1) Elegimos palabra secreta al azar
    palabra = random.choice(palabras)

    # 2) Configuración inicial de la partida
    vidas = 6                 # Cantidad de intentos fallidos permitidos
    acertadas = set()         # Letras correctas adivinadas
    falladas = set()          # Letras incorrectas intentadas
    intentos_palabra = set()  # Para guardar intentos de palabra completa y evitar repetirlos

    print("\n🎮 ¡Comienza el juego!")

    # 3) Loop principal del juego:
    # Continuamos mientras tengamos vidas y todavía no hayamos completado la palabra
    while vidas > 0 and not palabra_completa(palabra, acertadas):

        # --- Mostramos el estado actual al usuario ---
        print("\nPalabra:", mostrar_progreso(palabra, acertadas))
        print("Fallos :", " ".join(sorted(falladas)) if falladas else "(ninguno)")
        print("Vidas  :", vidas)

        # --- Pedimos un intento (letra o palabra) ---
        intento = pedir_intento()

        # Si la entrada fue inválida, volvemos al inicio del loop sin perder vida
        if intento is None:
            continue

        # =============================
        # CASO A: El usuario escribe 1 letra
        # =============================
        if len(intento) == 1:
            letra = intento

            # Si ya la intentó antes, avisamos y no hacemos nada
            if letra in acertadas or letra in falladas:
                print("ℹ️ Ya intentaste esa letra.")
                continue

            # Si la letra está en la palabra secreta => acierto
            if letra in palabra:
                acertadas.add(letra)
                print("✅ ¡Bien! La letra está.")
            else:
                # Si no está => fallo, restamos una vida
                falladas.add(letra)
                vidas -= 1
                print("❌ No está. Pierdes una vida.")

        # =============================
        # CASO B: El usuario escribe más de 1 letra => intenta la palabra completa
        # =============================
        else:
            # Si ya intentó exactamente esa palabra antes, avisamos
            if intento in intentos_palabra:
                print("ℹ️ Ya intentaste esa palabra completa.")
                continue

            # Guardamos este intento para no repetirlo
            intentos_palabra.add(intento)

            # Si coincide con la palabra secreta => gana instantáneo
            if intento == palabra:
                # Marcamos todas las letras como acertadas para salir del while
                acertadas.update(set(palabra))
                print("🎉 ¡Correcto! Adivinaste la palabra completa.")
            else:
                # Si no coincide => penalización (pierde 1 vida)
                vidas -= 1
                print("❌ No es la palabra. Pierdes una vida.")

    # 4) Al salir del loop, puede ser por victoria o derrota:
    if palabra_completa(palabra, acertadas):
        print("\n🏆 ¡Ganaste!")
        print("La palabra era:", palabra)
    else:
        print("\n💀 Perdiste. Te quedaste sin vidas.")
        print("La palabra era:", palabra)

def terminar():
    print("\n👋 Juego terminado por el usuario. ¡Hasta luego!")
    exit(0)

# =========================
# PROGRAMA PRINCIPAL
# =========================

def main():
    # Lista inicial de palabras (se puede modificar desde el menú)
    palabras = ["python", "ahorcado", "programacion", "gato", "computadora"]

    # Loop del menú principal:
    # Se repite hasta que el usuario elija "4"
    while True:
        opcion = mostrar_menu()

        if opcion == "1":
            # Opción 1: empezar una partida
            jugar(palabras)

        elif opcion == "2":
            # Opción 2: mostrar lista de palabras
            mostrar_palabras(palabras)

        elif opcion == "3":
            # Opción 3: agregar nueva palabra (si es válida)
            nueva = pedir_palabra_nueva()
            if nueva:
                if nueva in palabras:
                    print("ℹ️ Esa palabra ya está en la lista.")
                else:
                    palabras.append(nueva)
                    print("✅ Palabra agregada.")

        elif opcion == "4":
            # Opción 4: terminar el programa
            print("👋 ¡Hasta luego!")
            break

        else:
            # Si escribe cualquier cosa distinta a 1-4
            print("❌ Opción inválida. Elige 1, 2, 3 o 4.")


# Esto asegura que main() se ejecute solo si corres este archivo directamente:
# (y no si lo importas desde otro archivo)
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        terminar()