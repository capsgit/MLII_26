# 🧠 Fashion-MNIST – Model Evaluation Report
## 📌 Problem Definition

Clasificación multiclase de imágenes (28x28) en 10 categorías de prendas.

Tipo: clasificación supervisada
Métrica principal: accuracy
Métricas secundarias: F1-score, matriz de confusión

### 📊 Dataset
70,000 imágenes (60k train / 10k test)
Balanceado (~6,000 por clase)
Estructura: espacial (imagen)

### 🧪 Experimentos
🔹 Round 1 — MLP (baseline)
Input: flatten (784)
Modelo: Dense(512 → 128 → 10)
Accuracy: ~0.888

👉 Limitación: pierde estructura espacial

🔹 Round 2 — CNN básica
Conv(32) → Pool → Conv(64) → Pool
Accuracy: ~0.914

👉 Mejora clara → CNN captura estructura espacial

🔹 Round 3 — Más epochs
Epochs: 25
Accuracy: ~0.920

👉 Mejora por mayor entrenamiento

🔹 Last Round — CNN optimizada
3 bloques conv (32, 64, 128)
BatchNormalization
Dropout (0.3)
Data augmentation (rotation + zoom)
Learning rate: 0.0005

Accuracy: ~0.9168

### 📉 Observación clave

👉 Aunque la arquitectura es mejor, el accuracy baja ligeramente:

0.920 → 0.916

Pero:

👉 la matriz de confusión es mejor

### 🧠 Interpretación
❗ Esto NO es un empeoramiento real

Es:

👉 regularización funcionando
Antes (Round 3)
modelo más “confiado”
mayor accuracy
pero más riesgo de overfitting
Ahora (Last Round)
modelo más robusto
menos sobreajuste
mejor distribución de errores

### 🔍 Error Analysis

Errores principales:

0 ↔ 6 (t-shirt vs shirt)
2 ↔ 4 ↔ 6 (pullover / coat / shirt)

👉 errores estructurales del dataset

## 📊 Conclusión técnica
La familia correcta es CNN
El modelo final es estable y generaliza
El límite actual viene del dataset, no del modelo