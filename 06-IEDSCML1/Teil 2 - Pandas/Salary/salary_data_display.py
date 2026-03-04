from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

def load_cvs(path: str) -> pd.DataFrame:
# lee la data y crea un dataframe
    return pd.read_csv(Path(__file__).parent / path)

def plot_distribution(df: pd.DataFrame) -> None:
# muestra el histograma de todos los features/Columnas
    df.hist()
    plt.show()

def plot_scatter(df: pd.DataFrame, target: str) -> None:
    # plottea los Scatters de todas las Col. vs Target
    df.plot(kind = "scatter", x="experience_years", y=target, alpha=0.2)
    plt.show()

    df.plot(kind = "scatter", x="age", y=target, alpha=0.2)
    plt.show()

    df.plot(kind = "scatter", x="hours_per_week", y=target, alpha=0.2)
    plt.show()

def overwiew(df: pd.DataFrame) -> None:
# genera un resumen de la data a punta de prints->head/info/describe
    print("\n -----Head------------------")
    print(df.head())
    print("\n -----Info------------------")
    print(df.info())
    print("\n -----Vista estadistica------")
    print(df.describe())

if __name__ == "__main__":
    df = load_cvs("../data/salary_data.csv")
    overwiew(df)
    plot_distribution(df)
    plot_scatter(df, "salary")