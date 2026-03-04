"""
Breast Cancer Dataset aus scikit-learn untersuchen
https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic
"""

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import load_breast_cancer

data = load_breast_cancer()
df = pd.DataFrame(data.data, columns=data.feature_names)
df["class"] = data.target
print(data.target_names)  # [0 => 'malignant' 1=>'benign']
print(data.feature_names)

df = df[
    [
        "mean radius",
        "mean texture",
        "mean area",
        "mean smoothness",
        "mean concavity",
        "mean concave points",
        "class",
    ]
]
print(df.head())

def show_scatterplots(df: pd.DataFrame) -> None:
    pairs = [
        ("mean radius", "mean texture"),
        ("mean area", "mean smoothness"),
        ("mean concavity", "mean concave points"),
    ]
    _, axes = plt.subplots(1, len(pairs), figsize=(15, 4))
    for ax, (f1, f2) in zip(axes, pairs):
        ax.scatter(
            df[f1],
            df[f2],
            c=df["class"],
            cmap="viridis",
        )
        ax.set_xlabel(f1)
        ax.set_ylabel(f2)

    plt.legend()
    plt.tight_layout()
    plt.show()
