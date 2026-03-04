from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error


def load_csv(path: str) -> pd.DataFrame:
# lee la data y crea un dataframe
    df = pd.read_csv(Path(__file__).parent / path, index_col=0)
    return df

# a) Datensatz visualisieren
def prepare_data(df: pd.DataFrame, features: list[str], target: str) -> tuple[np.ndarray, np.ndarray]:
    # crear Feature_Matrix (X) & Target-Vector (y)
    X = df[features].to_numpy()
    y = df[target].to_numpy()
    """    print(df.head())
    print(" ----- " * 10)
    print(df.info())
    print(" ----- " * 10)
    print(df.describe())
    print(" ----- " * 10)
    print(X)
    print(" ----- " * 10)
    print(y)"""
    return X, y

def plot_distribution(df: pd.DataFrame) -> None:
# muestra el histograma de todos los features/Columnas
    df.hist()
    plt.tight_layout()
    plt.show()

def overwiew(df: pd.DataFrame) -> None:
# genera un resumen de la data a punta de prints->head/info/describe
    print("\n -----Head------------------")
    print(df.head())
    print("\n -----Info------------------")
    print(df.info())
    print("\n -----Vista estadistica------")
    print(df.describe())

def plot_scatter(df: pd.DataFrame, target: str) -> None:
    # plottea los Scatters de todas las Col. vs Target
    df.plot(kind = "scatter", x="TV", y=target, alpha=0.5, color="green")
    plt.show()

    df.plot(kind = "scatter", x="radio", y=target, alpha=0.5, color="violet")
    plt.show()

    df.plot(kind = "scatter", x="newspaper", y=target, alpha=0.5, color="blue")
    plt.show()

## b) Modell trainieren
def train_model(X_train: np.ndarray, y_train: np.ndarray) -> LinearRegression:
    # entrenar modelo
    model =LinearRegression()
    model.fit(X_train, y_train)
    return model

def evaluate_model(y_test, y_pred):
    # calificar
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred)

    print(f"\nR², erklärte Varianz: {r2:.2f}")

    # Durchschnittlicher absoluter Fehler, z.B. 4139.72 Euro liegt das Model daneben
    print(f"\nMAE: {mae:.2f}")

    # Quadratischer Fehler, schlecht interpretierbar
    print(f"\nMSE: {mse:.2f}")

    # MAPE: Mean absolute percentage Error (z.B. 0.11 => liegt 11% daneben)
    print(f"\nMAPE: {mape:.2f}")

## MAIN
def main():
    # cargar csv
    df = load_csv("data.csv")

    # generar titulo de columnas y
    features = ["TV", "radio", "newspaper"]
    X, y = prepare_data(df, features, "sales")

    # display
    overwiew(df)
    plot_distribution(df)
    plot_scatter(df, "sales")

    # Matrix de correlacion
    corr = df.corr(numeric_only=True)
    coef = df.corr(numeric_only=True)
    intercept = df.corr(numeric_only=True)
    print("\nCorrelacion: \n", corr)
    print("\nCoef: \n",coef)
    print("\nInterC \n", intercept)

    # regresion lineal
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = train_model(X_train, y_train)
    y_pred = model.predict(X_test)
    evaluate_model(y_test, y_pred)

    value = np.array([[230, 38, 70]])
    predict_sales = model.predict(value)
    print("\nPredicted sales: \n", predict_sales[0].round(2), "million Units")

if __name__ == "__main__":
    main()
