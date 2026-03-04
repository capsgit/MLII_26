"""
Breast Cancer Datensatz mit KNN
Wir nutzen eine Pipeline und GridSearch und Standard-Scaler
Standard-Scaler skaliert normalverteilte Daten auf die Standard-Normalverteilung
(alle Werte auf Mittelwert 0, Std. 1)

"""

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler

data = load_breast_cancer()
X, y = data.data, data.target

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

pipeline = Pipeline(
    [
        ("scaler", StandardScaler()),  # skaliert alle Werte auf Mittelwert 0, Std. 1
        ("knn", KNeighborsClassifier()),
    ]
)

param_grid = {
    # "scaler": [MinMaxScaler(), StandardScaler()], Beispiel für Scaler im GridSearch
    "knn__n_neighbors": [3, 5, 7, 9],
    "knn__weights": ["uniform", "distance"],
}

# GridSearch definieren
model = GridSearchCV(pipeline, param_grid, cv=5)

# Hier startet die GridSearch und ergebnis ist das trainerte Model
model.fit(X_train, y_train)

print("Besten Hyperparameter:", model.best_params_)  # in unserem FAll 5 Nachbarn

# Zum Testen (Vorhersagen) nutzen wir das ursprüngliche Test-Set
y_pred = model.predict(X_test)

# Klassifikationsreport printen auf Basis des y_test-Vektors und des vorhergesagten
# y_pred-Vektors
print(classification_report(y_test, y_pred))
