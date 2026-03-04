from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def read_data(file: str) -> pd.DataFrame:
    return pd.read_csv(Path(__file__).parent / file)

def prepare(X: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    return train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

def vectorize_text(train_text: np.ndarray, test_text: np.ndarray) -> tuple:
    """convertir texto Training & Test Data en features"""
    vectorizer = CountVectorizer()

    # fit: aprende
    # transform: convierte Traininsdaten en una matrix numerica
    X_train = vectorizer.fit_transform(train_text)

    # transform: usa el vocabulario ya aprendido  y no aprende mas palabras
    X_test = vectorizer.transform(test_text)
    return X_train, X_test, vectorizer

df = read_data("../data/spam.csv")
print(df.head())

# --------------------------------------------------------------
# ----------- Feature Matrix & Target Vector -------------------
# --------------------------------------------------------------
X = df["text"].to_numpy()
y = df["label"].to_numpy()

X_train, X_test, y_train, y_test = prepare(X, y)
X_train, X_test, vectorizer = vectorize_text(X_train, X_test)


print(X[:3], y[:3])
print("\nX \n", X_train[:3], "\ny \n", y_train[:3])
print("\nX_train \n", X_train[:3])
print()
print("\nX_test \n", X_test[:3])


# ----------------------------------------------------------
# -------------------- Model tranieren ---------------------
# ----------------------------------------------------------

model = MultinomialNB()
model.fit(X_train, y_train)

# predecir valores y reporte de clasificacion
y_pred = model.predict(X_test)

print("Modelo entrenado\n", y_pred[:3])
print()
print("classification_report: \n", classification_report(y_test, y_pred))

# los conceptos importantes que fueron definidos como SPAM
spam_log_probs = model.feature_log_prob_[0] # 1 => spam classe
top_ten = spam_log_probs.argsort()[:10]
features_names = vectorizer.get_feature_names_out()

for i in reversed(top_ten):
    print(f"{features_names[i]}: {spam_log_probs[i]:.2f}")