import pickle
from pathlib import Path

with open(Path(__file__).parent / "model.pkl", mode= "rb") as f:
    model = pickle.load(f)

print(model.predict([[5], [12]]))