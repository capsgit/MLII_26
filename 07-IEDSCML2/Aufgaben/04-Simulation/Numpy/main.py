# -------------------------------------------------------------------
# La logica se desarrolla en base a listas [] (numpy)
# -------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

DAYS = 7000
INITIAL_VALUE = 1.165


def calculate_index_change(initial_value: float, days: int) -> np.ndarray:
    """
    calcula la evolucion acumulada del indice
    """
    change_vector = np.random.normal(0, 0.02, days)
    series = [initial_value]
    current_value = initial_value

    for change in change_vector:
        current_value = current_value * (1 + change)
        series.append(current_value)

    return np.array(series)


def plot_index(series: np.ndarray):
    """
    Genera el gráfico de la evolución del índice.
    """
    d_axis = np.arange(len(series))

    plt.figure(figsize=(12, 6))
    plt.axhline(INITIAL_VALUE, linestyle="--", linewidth=0.8, color="yellow", label="Initial Value")

    for i in range(1, len(series)):

        if series[i] >= series[i - 1]:
            color = "green"
        else:
            color = "red"

        plt.plot(d_axis[i - 1:i + 1], series[i - 1:i + 1], color=color)

    plt.title("Simulated EUR vs USD Evolution")
    plt.xlabel("Days")
    plt.ylabel("EUR/USD")
    plt.scatter(series.argmax(), series.max()) # mostrar maximo
    plt.scatter(series.argmin(), series.min()) # mostrar minimo
    plt.plot(d_axis, np.poly1d(np.polyfit(d_axis, series, 1))(d_axis)) # mostrar tendencia media
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.4f')) # formato forex

    plt.grid(True, color="grey", linestyle="--", linewidth=0.5)
    plt.show()

def main ():
    series = calculate_index_change(INITIAL_VALUE, DAYS)
    plot_index(series)

if __name__ == "__main__":
    main()


