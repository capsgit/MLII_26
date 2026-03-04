"""
Visualisierung des Wine-Datensatzes.

Lade das Dataset, überführe es in ein DataFrame und analysiere es
grafisch. Erstelle Histogramme aller numerischen Features sowie
ausgewählte 2D-Streudiagramme, um Verteilungen, Skalierung und
Klassenstruktur visuell zu untersuchen.

1. Überführe die X-Daten in ein pandas DataFrame. Füge die y-Daten (targets) als
neue Spalte hinzu (df["class"] = y...)
2. Erzeuge Histogramme für alle Features.
3. Erstelle Scatterplots für mindestens zwei Feature-Paare
(z. B. alcohol vs. proline, magnesium vs. flavanoids).
4. optional: Färbe die Punkte nach Klasse (Recherche nach colormap)
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.pipeline import Pipeline

TEST_RATIO = 0.2
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
    # Datensatz laden
    data = datasets.load_wine()

    X = data.data
    y = data.target

    feature_names = data.feature_names

    # 1) convertir X en DataFrame (df)
    df = pd.DataFrame(X, columns=feature_names)
    df["class"] = y # agregar "y-daten" como columna

    # 2) histograma para cada feature
    df.drop(columns="class").hist(figsize=(12, 10)) # figsize=(12,10) Define el tamaño de la figura: ancho 12 alto 10 (inch)
    plt.tight_layout()  # ← ajuste automático del espacio. Solo “acomoda” el espacio para que títulos/labels no se monten
    plt.show()

    # 3-1) Scatter 1: alcohol vs proline
    plt.figure(figsize=(7, 5))
    sc1 = plt.scatter(df["alcohol"], df["proline"], c=df["class"], s=25, cmap="rainbow")
    plt.xlabel("alcohol")
    plt.ylabel("proline")
    plt.title("alcohol vs proline (colored by class)")
    plt.colorbar(sc1, label="class")
    plt.tight_layout()
    plt.show()

    # 3-2) Scatter 2: magnesium vs flavanoids
    plt.figure(figsize=(7, 5))
    sc2 = plt.scatter(df["magnesium"], df["flavanoids"], c=df["class"], cmap="viridis", s=25)
    plt.xlabel("magnesium")
    plt.ylabel("flavanoids")
    plt.title("magnesium vs flavanoids (colored by class)")
    plt.colorbar(sc2, label="class")
    plt.tight_layout()
    plt.show()

    """    
    # manuelles Splitting
    
    X_train, X_test, y_train, y_test = manual_train_test_split(X, y)
    model = KNeighborsClassifier(n_neighbors=K)  # inicializacion
    model.fit(X_train, y_train) # entreanar unicamente con Trainingsdaten
    predicted = model.predict(X_test) # se envia una "Matrix-Test-Feature" y se obtiene un "Klassen-Vektor"
    acc = accuracy_score(y_test, predicted)
    print(f"Accuracy: {acc:.2f}")
    cm = confusion_matrix(y_test, predicted)
    disp = ConfusionMatrixDisplay(cm)
    disp.plot()
    plt.show()

    print("confusion \n", classification_report(y_test, predicted))
    """

    # aufgabe 26.02.2026
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_RATIO,
        random_state=42,
        stratify=y,
    )

    pipeline_grid = Pipeline(
        [
            ("knn", KNeighborsClassifier()),
        ]
    )

    pipeline_knn = Pipeline(
        [
            ("knn", KNeighborsClassifier(n_neighbors=5)),
        ]
    )

    score = cross_val_score(pipeline_knn, X_train, y_train, cv=5)

    param_grid = {
        "knn__n_neighbors": [3, 5, 7, 9],
        "knn__weights": ["uniform", "distance"],
    }

    print("liste der Accurcy-Scores:", score)
    print("gemittelter Accuracy-Score:", score.mean())

    # GridSearch definieren
    model = GridSearchCV(pipeline_grid, param_grid, cv=5)


    # Hier startet die GridSearch und ergebnis ist das trainerte Model
    model.fit(X_train, y_train)
    print("Besten Hyperparameter: (solo gs)", model.best_params_)  # in unserem FAll 5 Nachbarn
    pipeline_knn.fit(X_train, y_train)


    # Zum Testen (Vorhersagen) nutzen wir das ursprüngliche Test-Set
    y_pred_gs = model.predict(X_test)
    y_pred_knn = pipeline_knn.predict(X_test)

    # Klassifikationsreport printen auf Basis des y_test-Vektors und des vorhergesagten
    # y_pred-Vektors
    print("GS: \n", classification_report(y_test, y_pred_gs))
    print("Knn: \n", classification_report(y_test, y_pred_knn))


if __name__ == "__main__":
    main()
