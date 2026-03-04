# app.py ?? data_cleaning.py
# ------------------------------------------------------------
# Runner/orquestador del cleaning.
#
# Idea:
#   - Aquí NO implementamos cleaning.
#   - Aquí SOLO ejecutamos el pipeline configurado y hacemos sanity checks.
#
# Flujo:
#   1) Crear DataCleaner con config/cleaning_config.json
#   2) df_clean = cleaner.clean_data()
#   3) Imprimir head + ejecutar quick_eda (verificación)
# ------------------------------------------------------------

from __future__ import annotations

__title__ = "Data Cleaning"
__version__ = "0.1.0"
__author__ = "capsgit"
__doc__ = """
The Application is desingned to clean an input CSV-file and export a new cleaned one
"""


import pandas as pd

from src.data_cleaner import DataCleaner


def quick_eda(df: pd.DataFrame) -> None:
    """
    EDA rápida (sanity check), NO ML.

    Objetivo:
      - Ver si el cleaning dejó los tipos bien
      - Ver si quedaron NA
      - Ver si hay valores absurdos
      - Confirmar rango temporal
      - Confirmar productos dominantes

    Esto ayuda a decidir después:
      - cuál target tendría sentido
      - qué features podrías crear
    """
    print("\n--- SHAPE ---")
    # (filas, columnas)
    print(df.shape)

    print("\n--- DTYPES ---")
    # Verifica que Quantity Ordered y Price Each sean numéricos
    # y Order Date sea datetime (si tu config lo castea)
    print(df.dtypes)

    print("\n--- NA COUNTS (top) ---")
    # Si el cleaning fue estricto, aquí debería salir vacío o muy pequeño.
    na = df.isna().sum().sort_values(ascending=False)
    print(na[na > 0].head(20))

    print("\n--- DATE RANGE ---")
    # Verifica si el dataset tiene fechas razonables
    if "Order Date" in df.columns:
        print(df["Order Date"].min(), "->", df["Order Date"].max())

    print("\n--- BASIC STATS (Quantity, Price) ---")
    # Describe numérico para detectar outliers ridículos
    cols = [c for c in ["Quantity Ordered", "Price Each"] if c in df.columns]
    if cols:
        print(df[cols].describe())

    print("\n--- TOP PRODUCTS ---")
    # Si Product existe, muestra top 10
    if "Product" in df.columns:
        print(df["Product"].value_counts().head(10))

def main() -> None:
    """
    Punto de entrada del script.

    """
    cleaner = DataCleaner("config/cleaning_config.json")
    df_clean = cleaner.clean_data()

    print("\n=== CLEANING DONE ===")
    print(df_clean.head())

    # sanity checks
    # quick_eda(df_clean)

if __name__ == "__main__":
    main()