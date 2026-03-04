"""
Animals Datensatz untersuchen / plotten
- lade CVS mit pandas
- scatterplots der wichtigsten Features
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

CVS_FILE = Path(__file__).parent/"data"/"animals.csv"

def main():
    df = pd.read_csv(CVS_FILE)
    print(df)

    cats = df[ df["label"] == "cat"]
    dogs = df[ df["label"] == "dog"]
    print("k", cats, "H", dogs)

# opc A -> con []
    plt.scatter(
        cats["snout_length"],
        cats["ear_length"],
        color = "red",
        label = "Cats")

# opc B -> con .
    plt.scatter(
        dogs.snout_length,
        dogs.ear_length,
        color = "blue",
        label = "Dogs"
    )

    plt.xlabel("Snout length in cm")
    plt.ylabel("Ear length in cm")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()



