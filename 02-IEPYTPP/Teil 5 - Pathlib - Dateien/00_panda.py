# -*- coding: utf-8 -*-
import pandas as pd

df_geladen = pd.read_excel("Hojas_varias.xlsx", sheet_name=None, engine="openpyxl")

#print(df_geladen)

for sheet, df in df_geladen.items():
    print(f"Blatt: {sheet}")
    print(df, "\n")