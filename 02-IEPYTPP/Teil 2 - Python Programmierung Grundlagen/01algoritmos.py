from __future__ import annotations


def leer_entero(mensaje: str, *, permitir_salir: bool = True) -> int:
    """
    Pide al usuario un número entero hasta que lo introduzca correctamente.
    Si permitir_salir=True, acepta 'q' para salir.
    """
    while True:
        texto = input(mensaje).strip()

        if permitir_salir and texto.lower() in {"q", "quit", "salir"}:
            raise SystemExit("Saliendo...")

        try:
            return int(texto)
        except ValueError:
            print("Entrada inválida: escribe un número entero (ej: 42, -7).")


def leer_divisor_no_cero(mensaje: str) -> int:
    """Pide un entero y obliga a que no sea 0."""
    while True:
        b = leer_entero(mensaje)
        if b != 0:
            return b
        print("El divisor no puede ser 0. Intenta otra vez.")


def div_normal(a: int, b: int) -> float:
    return a / b


def modulo(a: int, b: int) -> int:
    return a % b


def doble_div(a: int, b: int) -> int:
    return a // b


def division_manual(a: int, b: int) -> float:
    cociente = doble_div(a, b)
    resto = modulo(a, b)
    return cociente + (resto / b)


def main() -> None:
    a = leer_entero("Dame un número entero como dividendo (o 'q' para salir): ")
    b = leer_divisor_no_cero("Dame un número entero como divisor (≠ 0): ")

    div_normal_var = div_normal(a, b)
    modulo_var = modulo(a, b)
    doble_div_var = doble_div(a, b)
    manual_var = division_manual(a, b)

    ancho = 42
    print("-" * ancho)
    print(f"Dividendo: {a} | Divisor: {b}")
    print("-" * ancho)
    print(f"{'divNormal':<12}: {div_normal_var}")
    print(f"{'módulo':<12}: {modulo_var}  (parte frac: {modulo_var / b})")
    print(f"{'dobleDiv':<12}: {doble_div_var}")
    print(f"{'solución':<12}: {manual_var}")
    print("-" * ancho)

    # (Opcional) Comprobación: manual debe coincidir con / (salvo detalles de float)
    if abs(div_normal_var - manual_var) > 1e-12:
        print("Aviso: hay una pequeña diferencia por precisión de coma flotante.")


if __name__ == "__main__":
    main()
