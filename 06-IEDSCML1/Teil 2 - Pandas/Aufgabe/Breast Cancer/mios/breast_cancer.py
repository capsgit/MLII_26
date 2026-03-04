
"""
Breast

"""

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import load_breast_cancer
import seaborn as sns

data = load_breast_cancer()
print("Data: \n", data)

df = pd.DataFrame(data.data, columns=data.feature_names)
df["class"] = data.target


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

print("HEAD: \n", df.head(10))
print()
print("INFO: \n", df.info())
print()
print("DESCRIBE: \n", df.describe())
print()
print("Names: \n", data.target_names)

sns.pairplot(df, hue="class")
plt.show()

def show_scatter(df: pd.DataFrame) -> None:
    pairs = [
        ("mean radius", "mean texture"),
        ("mean area", "mean smoothness"),
        ("mean concavity", "mean concave points"),
    ]
    _, axes = plt.subplots(1, len(pairs), figsize=(15, 5))
    for ax, (f1, f2) in zip(axes, pairs):
        ax.scatter(df[f1], df[f2], c=df["class"], cmap="coolwarm", alpha=0.5)
        ax.set_xlabel(f1)
        ax.set_ylabel(f2)

    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    show_scatter(df)



if __name__ == "__main__":
    main()

