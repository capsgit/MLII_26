from sklearn.feature_extraction.text import CountVectorizer

texts = [
    "This is a sample",
    "The another sex",
    "Those sample rex",
    "Today ate one cut",
]

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(texts)

print("X\n", X)


# mostrar el vocabulario
vokabular = vectorizer.get_feature_names_out()
print("vokabular\n", vokabular)
print("Array\n", X.toarray())
print("0\n", len(texts[0]))
print("1\n", len(texts[1]))
print("2\n", len(texts[2]))
print("3\n", len(texts[3]))
print("Shape", X.toarray().shape)

# --------------------------------------------------------------------
# Feature-Matrix
# Jede Spalte ist ein Feature
#
# [[0 0 0 1 0 0 1 0 0 1 0 0]         # jede Zeile ist ein Dokument
#  [1 0 0 0 0 0 0 1 1 0 0 0]
#  [0 0 0 0 0 1 1 0 0 0 1 0]
#  [0 1 1 0 1 0 0 0 0 0 0 1]]
# --------------------------------------------------------------------

# print(X)  intern als Sparse Matrix gespeichert, um Vergeudung von Platz zu vermeiden
