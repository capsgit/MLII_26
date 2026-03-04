"""
Breast Cancer Datensatz mit SVM (SVC für Support Vector Classifiert)
Wir nutzen eine Pipeline und GridSearch und Standard-Scaler

"""

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import classification_report
from sklearn.svm import SVC
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
        ("svc", SVC()),
    ]
)

param_grid = {
    # "scaler": [MinMaxScaler(), StandardScaler()], Beispiel für Scaler im GridSearch
    "svc__C": [0.1, 1, 10],  # Stärke der Bestrafung der Fehlklassifikation
    "svc__gamma": ["scale", "auto"],
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
