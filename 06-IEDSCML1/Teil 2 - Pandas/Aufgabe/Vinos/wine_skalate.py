import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, GridSearchCV, cross_val_score, train_test_split
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay, accuracy_score


TEST_RATIO = 0.2

# Datensatz laden
data = datasets.load_wine()

# Definir X & y
X = data.data
y = data.target

# Train / Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_RATIO,
    random_state=42,
    stratify=y,
)

# PIPE-line
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("svm", SVC()),
])

# GridSearch para SVM (Support Vector Machine)
param_grid = [
    {"svm__kernel": ["linear"], "svm__C": [0.1, 1, 10, 100]},
    {"svm__kernel": ["rbf"], "svm__C": [0.1, 1, 10, 100], "svm__gamma": ["scale", "auto", 0.01, 0.1, 1]},
]

# BASEline CV
baseline_scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="accuracy")
print("\nBaseline CV mean: \n", baseline_scores.mean())

# GridSearch
gs = GridSearchCV(pipe, param_grid, cv=cv, scoring="accuracy", n_jobs=-1)
gs.fit(X_train, y_train)

print("\nBest params:\n", gs.best_params_)
print("\nBest CV score:\n", gs.best_score_)
print("\nBest estimator:\n", gs.best_estimator_)

# evaluacion FINAL
y_pred = gs.predict(X_test)
print("\nTest accuracy:\n", accuracy_score(y_test, y_pred))
print("\nTest classification:\n",classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
ConfusionMatrixDisplay(cm).plot()
plt.show()