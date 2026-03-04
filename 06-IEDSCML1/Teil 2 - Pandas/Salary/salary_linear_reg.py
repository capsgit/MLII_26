from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error

def load_cvs(path: str) -> pd.DataFrame:
    return pd.read_csv(Path(__file__).parent / path)

def prepare_data(df: pd.DataFrame, features: list[str], target: str) -> tuple[np.ndarray, np.ndarray]:
    # crear Feature_Matrix (X) & Target-Vector (y)
    X = df[features].to_numpy()
    y = df[target].to_numpy()
    print(df.head())
    return X, y

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

    print(f"R^2, erklärte Varianz: {r2:.2f}")

    # Durchschnittlicher absoluter Fehler, z.B. 4139.72 Euro liegt das Model daneben
    print(f"MAE: {mae:.2f}")

    # Quadratischer Fehler, schlecht interpretierbar
    print(f"MSE: {mse:.2f}")

    # MAPE: Mean absolute percentage Error (z.B. 0.11 => liegt 11% daneben)
    print(f"MAPE: {mape:.2f}")

if __name__ == "__main__":
    df = load_cvs("../data/salary_data.csv")
    features = ["age", "experience_years", "hours_per_week"]
    X, y = prepare_data(df, features, "salary")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = train_model(X_train, y_train)
    y_pred = model.predict(X_test)
    evaluate_model(y_test, y_pred)

    # estimar el salario del nuevo empleado
    #                 age, exp, h/w
    value = np.array([[30, 15, 32]])
    predict_salary = model.predict(value)
    print("$$$$ salario estimado para alguien con 30age, 6exp, 32h/w: \n", predict_salary.round(2), "€")
