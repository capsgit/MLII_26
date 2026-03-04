from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# Mini-Datensatz
texts = [
    "Win money now",
    "Cheap pills available",
    "Meeting tomorrow at 10",
    "Lunch with colleagues",
    "Earn money fast",
    "Project discussion",
]

labels = [1, 1, 0, 0, 1, 0]  # Spam  # Kein Spam

# Texto -> Numeros
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

# clasificador
model = MultinomialNB()
model.fit(X, labels)

# print("pre [0]\n", model.predict([texts[0]]))

# anticipar con Email-betreff si spam o no spam
msg = ["get free pills!", "Discussion pills", "sex free", "lunch tomorrow"]   # nuevo datapunto desconocido
X_new = vectorizer.transform(msg)   # convertirlo a vectores numericos
predicion = model.predict(X_new)

print("pos \n", predicion)
print()
print("pos cero \n", predicion[0])