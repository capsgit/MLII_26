"""
KNN - K-neareste Neighbours (Clasification)

Ablauf:
- Daten einlesen
- Feature-Matrix 'x' erzeugen & Label-Vector 'y' erzeugen
- Manuelles Train/Test Splitting
- KNN-Model erstellen (Instanz)
- Training mit Trainingsdaten (fit)
- Testen / Vorhersage (predict)
- Metriken anzeigen
"""


# |---------------------------DATEN-------------------------------|
# |--------------------80%-------------------||-------20%---------|
# |-Train/Model FIT -------------------------||-Test/Predict------|


from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay


CVS_FILE = Path(__file__).parent/"data"/"animals.csv"
TEST_RATIO = 0.2 # 20% test vs 80% train
K = 3

def manual_train_test_split(X: np.ndarray, y: np.ndarray) -> tuple:
    """Teil X und y im Training & Test"""

    np.random.seed(42)

    num_samples = X.shape[0]  # 20 => [9, 3, 0, 19, ...]
    test_size = int(num_samples * TEST_RATIO)

    indices = np.random.permutation(num_samples)
    train_idx = indices[:-test_size]
    test_idx = indices[-test_size:]

    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]


def main():
    df = pd.read_csv(CVS_FILE)

    # feature-Matrix & Label/Target-Vector
    X = df[["snout_length", "ear_length", "fur_density"]].to_numpy()
    y = df["label"].map({"dog": 0, "cat": 1}).to_numpy().astype(np.int8)

    # manuelles Splitting
    X_train, X_test, y_train, y_test = manual_train_test_split(X, y)

    # KNN-Model erstellen (instance)
    model = KNeighborsClassifier(n_neighbors=K) # inicializacion

    # Model trenieren (knn: Datenpunkte intern save)
    model.fit(X_train, y_train) # entreanar unicamente con Trainingsdaten

    # Vorhersagen (knn: Datenpunkte intern predict)
    predicted = model.predict(X_test) # se envia una "Matrix-Test-Feature" y se obtiene un "Klassen-Vektor"

    print(f"Matrix X: \n {X_test[:15]}")
    print("-"*20)
    print(f"Vector: {predicted}")

    # accurancy
    acc = accuracy_score(y_test, predicted)
    print("-"*20)
    print(f"Accuracy: {acc:.2f}")

    # confusion matrix plotten + show
    cm = confusion_matrix(y_test, predicted)
    disp = ConfusionMatrixDisplay(cm)
    disp.plot()
    plt.show()

    # clasification report with acc, f1, recall & precision
    print("confusion \n", classification_report(y_test, predicted))
    # (T = true, F = false, p = positive, n = negative)
    #               Tp  Fn   (0)        Fp   Tn  (1)
    # support (0)-> 51 + 4 = 55 || (1)-> 0 + 45 = 45



if __name__ == "__main__":
    main()



