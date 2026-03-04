## Übungsaufgabe: Lineare Regression mit dem Advertising-Datensatz

### Datensatz: Advertising

Der Advertising-Datensatz stammt aus dem Buch\
„An Introduction to Statistical Learning von James, Witten, Hastie et al.“ und
beschreibt den Zusammenhang zwischen Werbeausgaben und Verkaufszahlen.

**Features:**

- `TV`: Werbebudget für Fernsehwerbung (in Tausend Dollar)
- `radio`: Werbebudget für Radiowerbung (in Tausend Dollar)
- `newspaper`: Werbebudget für Zeitungswerbung (in Tausend Dollar)

**Target:**

- `sales`: Verkaufszahlen (in Tausend Einheiten)

Ziel des Datensatzes ist es, den Einfluss von Werbung auf den Verkauf mithilfe
**linearer Regression** zu untersuchen.

---

### Hinweis zum CSV-Format

Die CSV-Datei enthält eine Index-Spalte ohne Namen:

```csv
,TV,radio,newspaper,sales
1,230.1,37.8,69.2,22.1
2,44.5,39.3,45.1,10.4
```

Diese Spalte sollte als Index eingelesen werden.

Hilfsfunktion zum sauberen Einlesen:

```python
from pathlib import Path
import pandas as pd

def load_csv(path: str) -> pd.DataFrame:
    """Liest den Advertising-Datensatz ein."""
    df = pd.read_csv(Path(__file__).parent / path, index_col=0)
    return df
```

---

## a) Datensatz visualisieren

1. Lade den Datensatz mit der bereitgestellten `load_csv`-Funktion.
2. Verschaffe dir einen Überblick über die Daten:

   - `head()`
   - `info()`
   - `describe()`
3. Erstelle Histogramme für alle numerischen Spalten.
4. Erstelle Scatterplots:

   - `TV` vs. `sales`
   - `radio` vs. `sales`
   - `newspaper` vs. `sales`
5. Untersuche die Korrelationsmatrix.

**Ziel:**

- Verteilungen der Features verstehen
- Erste Einschätzung, welche Werbung den größten Einfluss auf `sales` hat

---

## b) Lineare Regression

1. Verwende `sales` als Target und die Werbebudgets als Features.
2. Teile die Daten in Trainings- und Testdaten.
3. Trainiere ein lineares Regressionsmodell.
4. Werte das Modell mit folgenden Metriken aus:

   - Mean Absolute Error (MAE)
   - Mean Squared Error (MSE)
   - R²-Score
