# -------------------------------------------------------------------
# La logica se desarrolla en base a Frames (xls)
# -------------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

DAYS = 7000
INITIAL_VALUE = 1.165

def create_exchange_rate_series_df(initial_value: float, days: int) -> pd.DataFrame:
    """
    Crea un DataFrame con la simulación de la evolución EUR/USD.
    """
    # Genera cambios aleatorios diarios.
    # np.random.normal(media, desviación, cantidad)
    # Aquí se simulan cambios porcentuales alrededor de 0
    changes = np.random.normal(0, 0.02, days)

    # Crea el DataFrame inicial
    df = pd.DataFrame({
        "day": np.arange(days),
        "change": changes
    })

    # Calcula el retorno acumulado
    # (1 + change).cumprod() multiplica todos los cambios sucesivos
    df["eur_usd"] = initial_value * (1 + df["change"]).cumprod()

    # Inserta el día 0 con el valor inicial
    first_row = pd.DataFrame({
        "day": [0],
        "change": [0],
        "eur_usd": [initial_value]
    })

    df.index = df.index + 1

    df = pd.concat([first_row, df], ignore_index=True)

    df = df.set_index("day")

    return df


def plot_exchange_rate(df: pd.DataFrame) -> None:
    """
    Genera el gráfico de la evolución simulada EUR/USD.
    """
    # Crea una figura con tamaño grande para que el gráfico sea legible
    plt.figure(figsize=(12, 6))

    # Dibuja una línea horizontal que marca el valor inicial
    # Esto ayuda a ver si el precio está por encima o por debajo del inicio
    plt.axhline(
        INITIAL_VALUE,
        linestyle="--",
        linewidth=0.8,
        color="yellow",
        label="Initial Value",
    )

    # Recorre la serie para colorear cada segmento del gráfico
    for i in range(1, len(df)):

        # Si el valor sube respecto al día anterior -> verde
        if df.iloc[i]["eur_usd"] >= df.iloc[i - 1]["eur_usd"]:
            color = "limegreen"
        else:
            # Si baja -> rojo
            color = "tomato"

        # Dibuja el segmento entre dos días consecutivos
        plt.plot(
            df.index[i - 1:i + 1],
            df["eur_usd"].iloc[i - 1:i + 1],
            color=color,
        )

    # Marca el punto donde el tipo de cambio alcanza su valor máximo
    plt.scatter(df["eur_usd"].idxmax(), df["eur_usd"].max())

    # Marca el punto donde alcanza su valor mínimo
    plt.scatter(df["eur_usd"].idxmin(), df["eur_usd"].min())

    # Calcula una línea de tendencia usando regresión lineal simple
    trend = np.poly1d(
        np.polyfit(df.index, df["eur_usd"], 1)
    )(df.index)

    # Dibuja la línea de tendencia
    plt.plot(df.index, trend)

    # Título del gráfico
    plt.title("Simulated EUR vs USD Evolution")

    # Etiqueta del eje horizontal
    plt.xlabel("Days")

    # Etiqueta del eje vertical
    plt.ylabel("EUR/USD")

    # Formatea el eje Y con 4 decimales (formato típico forex)
    plt.gca().yaxis.set_major_formatter(
        FormatStrFormatter("%.4f")
    )

    # Añade una cuadrícula suave para facilitar la lectura
    plt.grid(True, color="grey", linestyle="--", linewidth=0.5)

    # Muestra el gráfico en pantalla
    plt.show()


def main() -> None:
    # Crea el DataFrame con la simulación
    df = create_exchange_rate_series_df(INITIAL_VALUE, DAYS)
    print(df.head()) # Muestra las primeras filas para verificar los datos
    print()
    print(df.tail()) # Muestra las últimas filas del DataFrame

    # Genera el gráfico
    plot_exchange_rate(df)


if __name__ == "__main__":
    main()
