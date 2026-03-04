"""
Breast Cancer Datensatz mit KNN
Wir nutzen eine Pipeline, um die einzelnen Schritte sauber zu definieren.
"""

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline

data = load_breast_cancer()
X, y = data.data, data.target

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,  # proportionale Klassenverteilung bleibt erhalten
)

model = Pipeline(
    [
        ("knn", KNeighborsClassifier(n_neighbors=5)),
    ]
)

# in jedem von k-Läufen (k-cross-fold):
# wir nutzen 80% der (ursprünglichen) Trainingsdaten zum Training(Fitten) und
# 20% der (ursprünglichen) Trainingsdaten als Test (zur Validierung).
# Das ursprüngliche Testset (X_test, y_test) bleibt unberührt!
score = cross_val_score(model, X_train, y_train, cv=5)
# k scores [0.96703297 0.93406593 0.91208791 0.92307692 0.94505495]
print("liste der Accurcy-Scores:", score)
print("gemittelter Accuracy-Score:", score.mean())


# Wie gehabt das Model fitten und predicten
model.fit(X_train, y_train)

# Zum Testen (Vorhersagen) nutzen wir das ursprüngliche Test-Set
y_pred = model.predict(X_test)

# Klassifikationsreport printen auf Basis des y_test-Vektors und des vorhergesagten
# y_pred-Vektors
print(classification_report(y_test, y_pred))
