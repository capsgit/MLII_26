"""
California Housing Dataset
--------------------------------------------------------

Der California-Housing-Datensatz stammt ursprünglich aus einer Studie der
California Department of Housing aus den 1990er-Jahren. Er wurde von
scikit-learn aufbereitet und wird häufig für Machine-Learning-Übungen im
Bereich Regression genutzt.

Ziel des Datensatzes:
    Vorhersage des durchschnittlichen Hauswerts (Median House Value)
    basierend auf wenigen soziodemografischen und geografischen Merkmalen.

Features (Auszug):
    MedInc  – mittleres Einkommen im Gebiet
    HouseAge – durchschnittliches Alter der Häuser
    AveRooms – durchschnittliche Anzahl Zimmer
    Populaton – Bevölkerungszahl
    Latitude/Longitude – geografische Lage


"""

import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import scatter_matrix
from sklearn.datasets import fetch_california_housing


# --------------------------------------------------
# ---------------- Cargar Datensatz ----------------
# --------------------------------------------------
data = fetch_california_housing()
X = data.data
y = data.target
feature_names = data.feature_names

print("Feature-Namen:", feature_names)
print("Datenform:", X.shape)
print("\nAuszug X: \n", X[:5])
print("\nAuszug y:\n", y[:5])


# --------------------------------------------------
# ----------------- Crear DataFrame ----------------
# --------------------------------------------------
df = pd.DataFrame(X, columns=feature_names)
df["Target"] = y  # Hauswert

print(" -*-*-*-*-*- "* 8)
print()
print(df.head())
print()
df.info()
print()
print(df.isna().sum())
print()
print(df.describe().T)
print(" -*-*-*-*-*- "* 8)


# --------------------------------------------------
# ---------- Elegir features/columnas --------------
# --------------------------------------------------
cols = ["MedInc", "Latitude", "Longitude", "Target"]
missing = [c for c in cols if c not in df.columns]
if missing:
    raise ValueError(f"Estas columnas no existen en df: {missing}")

df_sel = df[cols].copy()
print("\n2)\n", df_sel.shape)


# --------------------------------------------------
# ----------- Sample (agilizar graficos) -----------
# --------------------------------------------------
RANDOM_STATE = 42
n = 3000  # prueba 2000-5000; si tu PC es potente, sube

df_plot = df_sel.sample(n=min(n, len(df_sel)), random_state=RANDOM_STATE)
print("\n3)\n", df_plot.shape)


# --------------------------------------------------
# -------------------- Pair-plot -------------------
# --------------------------------------------------
axes = scatter_matrix(
    df_plot,
    figsize=(12, 12),
    diagonal="hist",
    alpha=0.3,
    s=10,
)

plt.suptitle("California Housing - Scatter Matrix (sample)", y=1.02)
plt.show()


# --------------------------------------------------
# -------------- Matix de correlacion --------------
# --------------------------------------------------
corr = df_sel.corr(numeric_only=True)

plt.figure(figsize=(10, 8))
plt.imshow(corr, aspect="auto")
plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
plt.yticks(range(len(corr.index)), corr.index)
plt.colorbar()
plt.title("Correlation Matrix (California Housing)")
plt.tight_layout()
plt.show()

print("\nCorrelacion: \n", corr["Target"].sort_values(ascending=False))