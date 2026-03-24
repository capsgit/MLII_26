# 📋 MODELO_CHECKER_corregido.md
## Plantilla operativa para elegir, comparar e iterar modelos

---

## 🧭 Cómo usar este checker

Este archivo traduce el README a una secuencia ejecutable.
No reemplaza la explicación conceptual; la operacionaliza.

La numeración sigue esta lógica:

0. problema  
1. datos  
2. preprocesamiento  
3. familia de modelo  
4. baseline y comparación  
5. arquitectura  
6. entrenamiento  
7. evaluación  
8. interpretación  
9. generalización  
10. limitaciones  
11. control de errores  
12. iteración  

---

# 🎯 0. Definición del problema

## 0.1 Tipo de tarea
- [ ] Clasificación
- [ ] Regresión
- [ ] No supervisado

## 0.2 Objetivo concreto
- [ ] Está claro qué se quiere predecir o descubrir
- [ ] La variable objetivo está identificada
- [ ] Se entiende el costo del error

## 0.3 Métrica principal
- [ ] Está definida una métrica principal coherente con el problema
- [ ] La métrica elegida responde al costo real del error

Notas:
- Problema:
- Variable objetivo:
- Costo del error:

---

# 📊 1. Análisis de los datos

## 1.1 Tipo de dato
- [ ] Tabular
- [ ] Imagen
- [ ] Texto
- [ ] Series temporales
- [ ] Otro: ______________________

## 1.2 Tamaño y estructura
- [ ] Número de muestras revisado
- [ ] Número de features revisado
- [ ] Relación muestras / variables entendida
- [ ] Número de clases revisado (si aplica)

## 1.3 Calidad del dato
- [ ] Datos faltantes detectados
- [ ] Duplicados revisados
- [ ] Ruido aparente identificado
- [ ] Ejemplos corruptos / anómalos revisados

## 1.4 Distribución
- [ ] Clases balanceadas / desbalanceadas identificadas
- [ ] Distribución del target revisada
- [ ] Estructura relevante del dato revisada

## 1.5 Baseline razonable según el tipo de dato
- [ ] Existe un baseline simple definido
- [ ] El baseline corresponde al tipo de problema y dato
- [ ] El baseline sirve como referencia real para comparar mejoras

Notas:
- Tipo de dato:
- Baseline inicial:
- Señales de complejidad observadas:

---

# 🧹 2. Preprocesamiento

## 2.1 Escalado / normalización
- [ ] Se necesita escalado o normalización
- [ ] No se necesita escalado
- [ ] La decisión está justificada según el modelo

### Si se transforma la escala:
- [ ] StandardScaler
- [ ] MinMaxScaler
- [ ] Normalización a [0,1]
- [ ] Estandarización por canal
- [ ] Otro: ______________________

### Razón
- [ ] Modelo basado en distancia
- [ ] Modelo basado en margen
- [ ] Modelo basado en gradiente
- [ ] PCA
- [ ] Estabilidad numérica en redes
- [ ] Otro: ______________________

## 2.2 Variables categóricas
- [ ] Existen variables nominales
- [ ] Existen variables ordinales
- [ ] Se definió el encoding correcto
- [ ] Se revisó si hay alta cardinalidad
- [ ] No aplica

## 2.3 Datos faltantes
- [ ] Eliminación
- [ ] Imputación por media
- [ ] Imputación por mediana
- [ ] Imputación por moda
- [ ] Otro criterio
- [ ] No aplica

## 2.4 Outliers / anomalías
- [ ] Se identificaron
- [ ] Se eliminaron
- [ ] Se transformaron
- [ ] Se mantuvieron por decisión justificada
- [ ] No era un problema central para este tipo de dato

## 2.5 Reducción de dimensionalidad
- [ ] No aplica
- [ ] PCA
- [ ] Otra técnica

## 2.6 Transformación de estructura
- [ ] Imagen → normalización
- [ ] Imagen → flatten
- [ ] Imagen → mantener forma espacial
- [ ] Texto → vectorización
- [ ] Series → ventanas / lags
- [ ] Otro: ______________________

## 2.7 Control de leakage
- [ ] El preprocesamiento se ajusta solo sobre train
- [ ] Test y validation usan transformaciones derivadas del train

Notas:
- Preprocesamiento elegido:
- Justificación:
- Riesgos detectados:

---

# 🧠 3. Familia del modelo

## 3.1 Tipo de relación que parece existir
- [ ] Lineal o casi lineal
- [ ] No lineal basada en reglas
- [ ] No lineal compleja
- [ ] Alta dimensión con pocas muestras
- [ ] Estructura local / vecindad
- [ ] Estructura espacial
- [ ] Estructura temporal

## 3.2 Familia elegida
- [ ] Modelos lineales
- [ ] Árboles
- [ ] Random Forest
- [ ] Boosting
- [ ] SVM
- [ ] KNN
- [ ] MLP
- [ ] CNN
- [ ] RNN / LSTM / GRU
- [ ] Otra: ______________________

## 3.3 Justificación
- [ ] La familia elegida se conecta con la estructura del dato
- [ ] La familia elegida se conecta con la complejidad observada
- [ ] La familia elegida se conecta con el objetivo del problema

## 3.4 Regla práctica para imágenes
- [ ] Si se aplana la imagen, se justifica por qué no se usa estructura espacial
- [ ] Si la forma espacial importa, se considera CNN antes de escalar complejidad en MLP

Notas:
- Familia elegida:
- Razón principal:
- Señal que justificaría cambiar de familia:

---

# 🏗️ 4. Baseline y comparación

## 4.1 Modelo baseline
- [ ] Está definido
- [ ] Es razonable para el problema
- [ ] Su función es servir de referencia

### Modelo baseline:
- ________________________________________

## 4.2 Modelo alternativo / comparado
- [ ] Está definido
- [ ] Pertenece a la misma familia
- [ ] Pertenece a una familia distinta
- [ ] Existe justificación del cambio

### Modelo alternativo:
- ________________________________________

## 4.3 Control experimental
- [ ] No se cambian demasiadas variables a la vez
- [ ] La comparación es interpretable
- [ ] El cambio de modelo responde a una hipótesis

Notas:
- Hipótesis de comparación:
- Qué se espera mejorar:
- Qué señal invalidaría este cambio:

---

# 🧩 5. Arquitectura del modelo

> Esta sección aplica sobre todo a redes y modelos de capacidad configurable.

## 5.1 Capacidad
- [ ] Se definió número de capas
- [ ] Se definió número de neuronas o filtros
- [ ] Se entiende qué capacidad representa esa elección

## 5.2 Activaciones
- [ ] ReLU
- [ ] Tanh
- [ ] Sigmoid
- [ ] Softmax
- [ ] Leaky ReLU
- [ ] Otra: ______________________

## 5.3 Coherencia arquitectura ↔ problema
- [ ] La capacidad no parece insuficiente
- [ ] La capacidad no parece excesiva
- [ ] Existe una razón para la activación elegida
- [ ] La arquitectura respeta la estructura del dato

Notas:
- Arquitectura:
- Activación:
- Riesgo principal esperado (underfit / overfit / inestabilidad):

---

# ⚙️ 6. Configuración del entrenamiento

## 6.1 Optimizer
- [ ] Adam
- [ ] SGD
- [ ] RMSprop
- [ ] Adagrad
- [ ] Otro: ______________________

## 6.2 Learning rate
- [ ] Está definido
- [ ] Está justificado
- [ ] Se observó su efecto sobre la estabilidad

Valor:
- ______________________

## 6.3 Batch size
- [ ] Está definido
- [ ] Es coherente con hardware y objetivo
- [ ] Se entiende su efecto esperado

Valor:
- ______________________

## 6.4 Epochs
- [ ] No se eligieron arbitrariamente
- [ ] Se observan con train/validation
- [ ] Existe criterio para detener o continuar

Valor inicial:
- ______________________

## 6.5 Regularización
- [ ] No aplica
- [ ] L2
- [ ] Dropout
- [ ] Early stopping
- [ ] Data augmentation
- [ ] Batch Normalization
- [ ] Otra: ______________________

## 6.6 División de datos
- [ ] Train
- [ ] Validation
- [ ] Test
- [ ] Validación cruzada (si aplica)

## 6.7 Coherencia global
- [ ] El entrenamiento está alineado con la arquitectura
- [ ] El entrenamiento está alineado con el riesgo esperado
- [ ] La configuración permite diagnosticar overfitting / underfitting

Notas:
- Configuración elegida:
- Primer síntoma observado:
- Ajuste más probable si falla:

---

# 📈 7. Evaluación

## 7.1 Métricas
- [ ] Accuracy
- [ ] Precision
- [ ] Recall
- [ ] F1
- [ ] MAE
- [ ] MSE / RMSE
- [ ] Otra: ______________________

## 7.2 Curvas
- [ ] Train loss
- [ ] Validation loss
- [ ] Train accuracy
- [ ] Validation accuracy

## 7.3 Errores específicos
- [ ] Matriz de confusión
- [ ] Clases problemáticas
- [ ] Residuales (si regresión)
- [ ] Ejemplos mal clasificados

## 7.4 Lectura preliminar
- [ ] Train mal + val mal
- [ ] Train bien + val mal
- [ ] Entrenamiento inestable
- [ ] Mejora razonable y estable

Notas:
- Métrica principal observada:
- Patrón en curvas:
- Tipo de error dominante:

---

# 🧠 8. Interpretación

## 8.1 Diagnóstico principal
- [ ] Underfitting
- [ ] Overfitting
- [ ] Inestabilidad
- [ ] Ganancia marginal frente al baseline
- [ ] Resultado razonable

## 8.2 Acción sugerida
- [ ] Más capacidad
- [ ] Menos capacidad
- [ ] Más regularización
- [ ] Menos regularización
- [ ] Ajustar learning rate
- [ ] Cambiar de familia
- [ ] Mantener modelo actual

## 8.3 Justificación
- [ ] La acción elegida se apoya en métricas
- [ ] La acción elegida se apoya en curvas
- [ ] La acción elegida se apoya en errores concretos

Notas:
- Interpretación:
- Acción:
- Razón:

---

# 🌍 9. Generalización

## 9.1 Control de generalización
- [ ] Existe test set
- [ ] Existe validación cruzada si era necesaria
- [ ] No se concluye solo con train
- [ ] El resultado fuera de muestra es aceptable

Notas:
- Resultado en test:
- Diferencia train/validation/test:
- Riesgo de sobreajuste a validation:

---

# ⚠️ 10. Limitaciones

- [ ] Tamaño del dataset limitado
- [ ] Sesgo de muestreo posible
- [ ] Ruido alto
- [ ] Variables faltantes relevantes
- [ ] Split frágil
- [ ] Poco respaldo estadístico
- [ ] Otra: ______________________

Notas:
- Limitación principal:
- Cómo afecta la conclusión:

---

# 🧪 11. Errores comunes (control interno)

- [ ] Se evitó usar una sola métrica
- [ ] Se evitó comparar con splits distintos
- [ ] Se evitó cambiar demasiadas cosas a la vez
- [ ] Se evitó ignorar el baseline
- [ ] Se revisaron errores específicos
- [ ] Se alineó la métrica con el costo del error
- [ ] Se evitó confundir mejora real con más complejidad sin justificación

---

# 🔁 12. Iteración

## Si el diagnóstico es underfitting:
- [ ] aumentar capacidad
- [ ] entrenar más
- [ ] mejorar features
- [ ] cambiar de familia si hace falta

## Si el diagnóstico es overfitting:
- [ ] regularizar
- [ ] simplificar
- [ ] usar early stopping
- [ ] conseguir más datos

## Si el diagnóstico es inestabilidad:
- [ ] bajar LR
- [ ] revisar escalado / normalización
- [ ] revisar batch size
- [ ] revisar arquitectura

## Si el baseline ya es suficiente:
- [ ] detener escalada de complejidad
- [ ] documentar por qué el modelo simple basta

Notas finales de iteración:
- Qué se mantiene:
- Qué cambia:
- Qué hipótesis se prueba en la siguiente ronda:

---

# 📌 Regla final

Si no puede explicarse por qué un modelo funciona mejor que otro,
no se ha realizado una comparación de modelos; solo se ha ejecutado código.
