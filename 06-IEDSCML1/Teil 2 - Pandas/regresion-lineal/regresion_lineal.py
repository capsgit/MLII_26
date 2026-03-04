import pickle
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

X = np.array(
    [
        [0],
        [1],
        [2],
        [3],
        [4]
    ]
)
y = np.array([1, 3, 2, 5, 7])

model = LinearRegression()
model.fit(X, y) # encontrado ahora // aca se entrena el modelo

x_line = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
y_line = model.predict(x_line)

# plot
plt.scatter(X, y, color="black")
plt.plot(x_line, y_line, color="red")
plt.show()

print("Y-Achsenabschnitt: ", model.intercept_)
print("Steigung: ", model.coef_[0])

# Model saved con PICKEL
with open(Path(__file__).parent / "model.pkl", mode= "wb") as f:
    pickle.dump(model, f)