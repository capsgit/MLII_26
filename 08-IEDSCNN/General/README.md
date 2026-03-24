# 🧠 Modellvergleich en Machine Learning  
## Guía larga para orientarse entre datos, modelos, entrenamiento y evaluación

---

## 🧭 Cómo usar este documento

Este README **no** es una chuleta corta ni un resumen de definiciones.  
Su propósito es funcionar como **marco de razonamiento** para responder, de forma ordenada, a estas preguntas:

1. ¿Qué problema se está resolviendo realmente?
2. ¿Qué tipo de datos se tienen?
3. ¿Qué familia de modelos tiene sentido en ese espacio?
4. ¿Qué algoritmo concreto conviene probar primero?
5. ¿Cómo debe configurarse el entrenamiento?
6. ¿Cómo debe evaluarse el comportamiento del modelo?
7. ¿Qué señal indica que debe simplificarse, complejizarse o cambiarse de familia?

El flujo lógico que estructura el documento es el siguiente:

```text
problema
   ↓
datos
   ↓
preprocesamiento
   ↓
familia de modelo
   ↓
modelo concreto
   ↓
arquitectura (si aplica)
   ↓
configuración del entrenamiento
   ↓
evaluación
   ↓
interpretación
   ↓
ajustes
   ↓
iteración
```

📌 Este archivo explica el **por qué** de cada decisión.  
📋 El archivo `MODELO_CHECKER.md` convierte esa lógica en una **plantilla operativa y checklist de ejecución**.

---

## 📚 Índice

- [🎯 0. Definición del problema](#-0-definición-del-problema)
- [📊 1. Análisis de los datos](#-1-análisis-de-los-datos)
- [🧹 2. Preprocesamiento](#-2-preprocesamiento)
- [🧠 3. Familia del modelo](#-3-familia-del-modelo)
- [🏗️ 4. Modelo concreto](#️-4-modelo-concreto)
- [🧩 5. Arquitectura del modelo](#-5-arquitectura-del-modelo)
- [⚙️ 6. Configuración del entrenamiento](#️-6-configuración-del-entrenamiento)
- [📈 7. Evaluación](#-7-evaluación)
- [🧠 8. Interpretación](#-8-interpretación)
- [🌍 9. Generalización](#-9-generalización)
- [⚠️ 10. Limitaciones](#️-10-limitaciones)
- [🧪 11. Errores comunes](#-11-errores-comunes)
- [🔁 12. Lógica completa de iteración](#-12-lógica-completa-de-iteración)
- [📌 Regla final](#-regla-final)

---

# 🎯 0. Definición del problema

La primera decisión no consiste en elegir un algoritmo, sino en determinar **qué tipo de salida se espera** y **qué tipo de estructura pretende aprenderse**.

## 0.1 Tipos generales de problema

| Tipo de problema | Salida esperada | Pregunta típica | Ejemplos de modelos |
|---|---|---|---|
| Clasificación | Categoría o etiqueta | ¿A qué clase pertenece esta observación? | Logistic Regression, SVM, árboles, RF, boosting, redes |
| Regresión | Valor continuo | ¿Qué valor numérico debe predecirse? | Linear Regression, árboles, RF, boosting, redes |
| No supervisado | Agrupación, estructura o compresión | ¿Qué organización interna tienen los datos? | KMeans, PCA, clustering jerárquico, autoencoders |

## 0.2 Qué define esta sección

La definición del problema condiciona:

- la forma de la salida del modelo
- la función de pérdida
- las métricas relevantes
- la manera de interpretar el error
- la familia de modelos con sentido

## 0.3 Ejemplos mínimos

| Tipo | Ejemplo | Naturaleza del error importante |
|---|---|---|
| Clasificación | spam / no spam | falsos positivos o falsos negativos |
| Regresión | precio de vivienda | magnitud del error |
| No supervisado | segmentación de clientes | coherencia de los grupos o compresión |

🔗 **Conexión con la sección 1:**  
Una vez definido el tipo de problema, la siguiente pregunta ya no es “qué modelo usar”, sino:

> **¿Qué estructura tienen los datos con los que se intentará resolver ese problema?**

---

# 📊 1. Análisis de los datos

El modelo no se elige en abstracto.  
Se elige en relación con:

- el tamaño del dataset
- el tipo de variable
- la complejidad de la relación entre variables
- la presencia de ruido, outliers o correlación
- la necesidad de interpretabilidad

## 1.1 Modelo mental: tipo de dato → espacio de modelos posibles

| Tipo de dato | Descripción | Modelos que suelen tener sentido | Cuándo usar modelos simples | Cuándo usar modelos complejos | Señales para cambiar de modelo | Baseline recomendado |
|---|---|---|---|---|---|---|
| 📊 Tabular | Filas y columnas: edad, salario, variables estructuradas | Logistic/Linear Regression, Decision Tree, Random Forest, XGBoost/LightGBM/CatBoost, SVM, MLP | Pocos datos, relación aparentemente simple, necesidad de interpretabilidad | Interacciones fuertes, no linealidad, muchas variables, rendimiento insuficiente | Underfitting lineal, errores sistemáticos, patrón no capturado | Logistic / Linear |
| 🖼️ Imagen | Datos con estructura espacial local | CNN, transfer learning, MLP como baseline | Ejercicio didáctico, baseline rápido, dataset muy pequeño o simple | Problemas reales de visión, patrones espaciales complejos, clases similares visualmente | MLP no captura bordes, formas o texturas | MLP simple |
| 📝 Texto | Datos secuenciales con carga semántica | TF-IDF + Logistic Regression, SVM, embeddings, transformers | Dataset pequeño, problema simple, necesidad de interpretabilidad | Contexto semántico complejo, tareas avanzadas de NLP | Confusión semántica, dependencia contextual mal capturada | TF-IDF + Logistic |
| ⏱️ Series temporales | Datos dependientes del tiempo | ARIMA/SARIMA, modelos con features temporales, LSTM/GRU, transformers temporales | Patrones simples, estacionalidad clara, necesidad de interpretabilidad | Dinámica compleja, múltiples series, dependencia larga | Predicción inestable, mala captura de tendencia o estacionalidad | valor previo / media móvil |

## 1.2 Complejidad del dataset → capacidad inicial del modelo

| Condición observada | Consecuencia razonable |
|---|---|
| pocos datos | conviene comenzar con modelos simples y regularizados |
| mucha no linealidad aparente | conviene probar árboles, RF o boosting |
| muchas features y pocas muestras | conviene probar SVM o modelos lineales regularizados |
| gran complejidad estructural | conviene considerar boosting o redes |
| necesidad fuerte de interpretabilidad | conviene priorizar modelos lineales o árboles |

## 1.3 Variables importantes a inspeccionar

### Tamaño
- número de muestras
- número de features
- relación muestras / variables

### Distribución
- clases balanceadas o no
- distribución de target
- dispersión de variables

### Calidad
- datos faltantes
- ruido
- outliers
- duplicados

### Dependencia
- correlaciones
- multicolinealidad
- estructura temporal
- estructura espacial

## 1.4 Razón de ser de esta sección

Esta sección no escoge todavía el algoritmo.  
Su función es responder:

> **qué tan simple o compleja parece ser la función que conecta inputs y outputs**

🔗 **Conexión con la sección 2:**  
Una vez entendido el tipo de dato y su complejidad, la siguiente pregunta es:

> **¿Qué transformaciones deben aplicarse para que el modelo pueda aprender bien?**

---

# 🧹 2. Preprocesamiento

El preprocesamiento no es un ritual fijo.  
No existe una receta universal que se aplique igual a cualquier problema.

Su función es:

- volver comparables las variables cuando el modelo lo exige
- codificar correctamente la información categórica
- reducir ruido o redundancia
- adaptar la estructura del dato a la familia de modelos

## 2.1 Escalado

### Cuándo suele ser necesario

| Modelo / familia | ¿Requiere escalado? | Razón |
|---|---|---|
| KNN | Sí | depende de distancia |
| SVM / SVC / SVR | Sí | depende de margen y geometría |
| Logistic / Linear con regularización | Sí, recomendable | optimización más estable e interpretación comparable de coeficientes |
| Redes neuronales | Sí, normalmente | estabilidad del gradiente y del entrenamiento |
| PCA | Sí, normalmente | depende de varianzas relativas |
| Árboles / RF / boosting basado en árboles | No | usan umbrales y particiones |

### Explicación conceptual

Los modelos basados en distancia, margen o gradiente son sensibles a la escala.  
Los árboles no comparan magnitudes globales: hacen particiones por umbrales.

### Regla operativa
- Escalar en KNN, SVM, redes y modelos lineales cuando la escala entre variables sea heterogénea.
- No escalar por reflejo en árboles.

## 2.2 Tipos de escalado

| Método | Qué hace | Cuándo conviene |
|---|---|---|
| StandardScaler | centra en media 0 y varianza 1 | opción general, especialmente en modelos lineales, SVM, PCA |
| MinMaxScaler | lleva a un rango acotado, típico 0–1 | redes neuronales, casos donde interesa rango fijo |
| Normalización por máximo teórico | ejemplo: dividir por 255 | imágenes y variables con rango físico claro |

### Diferencia conceptual
- **StandardScaler** estandariza
- **MinMaxScaler** reescala
- la “normalización” de imágenes suele ser una variante sencilla de reescalado

## 2.3 Variables categóricas

| Tipo de variable | Método recomendado | Razón |
|---|---|---|
| Nominal | One-hot encoding | evita imponer orden artificial |
| Ordinal | Label encoding / codificación ordinal | preserva relación de orden |

### Alta cardinalidad
Cuando la variable tiene muchísimas categorías:
- one-hot puede explotar dimensionalidad
- puede ser mejor considerar:
  - target encoding
  - hashing
  - embeddings
  - codificaciones específicas según contexto

⚠️ Error clásico: usar label encoding en una variable nominal, introduciendo un orden inexistente.

## 2.4 Reducción de dimensionalidad

### PCA

| Conviene usar PCA cuando… | Conviene evitar PCA cuando… |
|---|---|
| hay muchas variables correlacionadas | la interpretabilidad de cada variable es crítica |
| existe mucho ruido | un modelo de árbol ya maneja bien la complejidad |
| interesa simplificar o visualizar | la compresión destruye información útil |

### Matiz importante
En árboles no suele ser obligatorio, pero tampoco está “prohibido”.  
Puede ayudar si hay ruido extremo o dimensionalidad muy alta, aunque normalmente no es la primera herramienta.

## 2.5 Datos faltantes

Opciones típicas:
- eliminar filas o columnas
- imputar con media, mediana o moda
- imputación más sofisticada según contexto

La elección depende de:
- porcentaje faltante
- patrón del faltante
- importancia de la variable
- sensibilidad del modelo

## 2.6 Outliers

| Familia de modelos | Sensibilidad a outliers |
|---|---|
| Regresión lineal | alta |
| KNN | alta |
| SVM | alta o moderada según kernel y escala |
| Árboles / RF / boosting | relativamente menor |

Acciones posibles:
- eliminar
- winsorizar
- transformar
- cambiar de familia de modelo
- usar métricas robustas

## 2.7 Transformación de estructura

| Tipo de dato | Transformación común |
|---|---|
| Imagen | normalización y, si se usa MLP, flatten |
| Texto | vectorización, embeddings |
| Series | ventanas temporales, lags, rolling features |

🔗 **Conexión con la sección 3:**  
Una vez preparado el dato, la pregunta ya no es “qué limpieza hacer”, sino:

> **qué tipo de relación entre variables se espera que el modelo capture**

---

# 🧠 3. Familia del modelo

Esta sección **no** elige todavía un algoritmo específico.  
Define algo anterior y más importante:

> **qué tipo de función o estructura de relación se considera plausible para el problema**

Aquí es donde se decide si la situación parece resolverse mejor con:
- una relación lineal
- reglas no lineales
- ensamblados
- vecindad
- márgenes en alta dimensión
- aproximación universal
- estructura espacial
- estructura temporal

## 3.1 Relación en los datos → familia de modelo

| Tipo de relación | Familia de modelo | Cuándo usar | Ventaja principal | Riesgo principal | Señales para cambiar |
|---|---|---|---|---|---|
| Lineal o casi lineal | Modelos lineales | baseline, interpretabilidad, pocos datos | simple y explicable | underfitting | patrones sistemáticos no capturados |
| No lineal basada en reglas | Árboles | umbrales, reglas if-then, interpretabilidad | reglas claras | overfitting, alta varianza | comportamiento inestable |
| No lineal ensamblada | Random Forest | robustez, tabular general | estable y fuerte | más pesado, menos interpretable | mejora limitada frente al baseline |
| No lineal compleja | Boosting | tabular difícil, máximo rendimiento | muy potente | tuning delicado | overfitting o ganancia marginal |
| Frontera compleja en alta dimensión | SVM | pocas muestras, muchas features | margen fuerte | escala mal con muchos datos | entrenamiento lento o sensibilidad alta |
| Local / vecindad | KNN | estructura local clara | simple e intuitivo | mala escalabilidad y mal rendimiento en alta dimensión | desempeño pobre con muchas features |
| Aproximación universal | MLP / redes densas | patrones complejos con suficiente dato | flexible | tuning difícil, inestabilidad | overfitting o inferior a boosting en tabular |
| Espacial | CNN | imágenes y patrones locales | explota estructura espacial | requiere más datos o transferencia | MLP falla en visión |
| Temporal / secuencial | RNN / LSTM / GRU / modelos temporales | dependencias de secuencia o tiempo | modela dependencia temporal | entrenamiento difícil | inestabilidad o captura temporal insuficiente |

## 3.2 Razón de ser de esta tabla

La tabla de “familia del modelo” conecta dos mundos:

- lo observado en los datos
- la estructura matemática que el modelo deberá aproximar

Sin esta capa intermedia, la elección de algoritmo se vuelve arbitraria.

## 3.3 Qué decide esta sección

Esta sección responde:

- ¿conviene empezar por una hipótesis lineal?
- ¿hacen falta reglas y particiones?
- ¿conviene un ensamblado?
- ¿la complejidad justifica una red?
- ¿hay una estructura espacial o temporal que un modelo genérico perdería?

🔗 **Conexión con la sección 4:**  
Una vez elegida la familia, la siguiente pregunta sí es concreta:

> **qué algoritmo específico conviene seleccionar dentro de esa familia**

---

# 🏗️ 4. Modelo concreto

Aquí ya no se discute la familia abstracta, sino el algoritmo puntual que se probará.

Esta sección debe permanecer alineada con la lógica del `MODELO_CHECKER.md`:

- primero baseline
- luego alternativa razonable dentro o fuera de la familia
- luego comparación controlada
- luego ajuste o cambio si el diagnóstico lo exige

## 4.1 Jerarquía práctica de selección

| Nivel de decisión | Modelo concreto típico | Función dentro del proceso |
|---|---|---|
| 1 | Logistic / Linear Regression | baseline interpretable |
| 2 | Decision Tree / Random Forest | capturar no linealidad con estructura relativamente manejable |
| 3 | XGBoost / LightGBM / CatBoost | búsqueda de rendimiento fuerte en tabular |
| 4 | SVM | frontera compleja con pocas muestras o alta dimensión |
| 5 | MLP / CNN / modelos de secuencia | máxima flexibilidad cuando la estructura del dato lo justifica |

## 4.2 Qué significa “baseline”

Un baseline no es el modelo “correcto”; es el punto de referencia mínimo razonable.

Sirve para:
- saber si el problema ya se resuelve con baja complejidad
- medir la ganancia real de modelos más sofisticados
- detectar underfitting de manera clara
- evitar saltar a complejidad sin justificación

## 4.3 Tabla comparativa de familias concretadas

| Modelo concreto | Cuándo usar | Ventaja | Riesgo | Señal de sustitución |
|---|---|---|---|---|
| Logistic / Linear | baseline, interpretabilidad | simple, rápido | puede quedarse corto | error sistemático, no linealidad fuerte |
| Decision Tree | reglas e interpretabilidad | fácil de explicar | sobreajusta | alta varianza, resultados inestables |
| Random Forest | robustez y tabular general | fuerte y estable | pesado y menos interpretable | mejora insuficiente frente a complejidad |
| Boosting | tabular exigente | alto rendimiento | tuning delicado | overfitting o beneficio marginal |
| SVM | alta dimensión, pocas muestras | potente en margen | escala mal | costo computacional o sensibilidad extrema |
| KNN | baseline local | intuitivo | sufre en alta dimensión | bajo rendimiento sistemático |
| MLP | flexibilidad general | aproxima relaciones complejas | inestable, tuning alto | inferior a boosting o sobreajuste |
| CNN | imágenes | explota estructura espacial | requiere datos/cómputo | dataset demasiado pequeño sin transferencia |
| LSTM/GRU | dependencia temporal | modela secuencia | entrenamiento más frágil | mala captura temporal o inestabilidad |

## 4.4 Regla operativa de esta sección

No conviene saltar directamente al modelo más complejo.

La lógica razonable es:
1. establecer baseline
2. medir insuficiencia
3. mover a una familia más capaz
4. volver a medir

🔗 **Conexión con la sección 5:**  
Una vez elegido el algoritmo, la siguiente pregunta es:

> **qué capacidad interna tendrá ese modelo y cómo se parametriza su forma de aprendizaje**

---

# 🧩 5. Arquitectura del modelo

Esta sección aplica sobre todo a modelos paramétricos configurables, especialmente redes neuronales.  
En modelos clásicos, parte de esta lógica se traduce a profundidad, regularización o complejidad estructural.

## 5.1 Qué significa arquitectura

La arquitectura define:
- la capacidad del modelo
- el tipo de composiciones internas que puede aprender
- el equilibrio entre bias y varianza

## 5.2 Capacidad: capas y neuronas

| Parámetro | Configuración baja | Configuración alta | Consecuencia |
|---|---|---|---|
| Capas | modelo simple | modelo jerárquico | más profundidad = más expresividad y más riesgo |
| Neuronas | compacto | gran capacidad | más capacidad = menor bias potencial, mayor varianza |

### Idea central
- más capacidad no significa automáticamente mejor rendimiento
- una arquitectura demasiado grande puede memorizar
- una arquitectura demasiado pequeña puede subajustar

## 5.3 Activaciones

| Función | Uso típico | Ventaja | Riesgo o limitación |
|---|---|---|---|
| ReLU | capas ocultas | simple, rápida, estándar | neuronas muertas |
| Tanh | alternativa en capas ocultas | centrada en cero | saturación |
| Sigmoid | salida binaria | probabilidad binaria | saturación en capas ocultas |
| Softmax | salida multiclase exclusiva | distribución sobre clases | no aplica a multilabel |
| Leaky ReLU | alternativa a ReLU | evita gradiente nulo negativo | menor simplicidad interpretativa |
| GELU / ELU | variantes modernas | suavidad o rendimiento potencial | complejidad innecesaria en problemas básicos |

## 5.4 Relación arquitectura ↔ comportamiento

| Señal observada | Posible lectura arquitectónica |
|---|---|
| train y validation pobres | arquitectura insuficiente o features pobres |
| train muy alto y validation baja | capacidad excesiva o regularización insuficiente |
| entrenamiento inestable | arquitectura difícil de optimizar o LR inadecuado |

## 5.5 Razón de ser de esta sección

La arquitectura responde a:

> **qué puede aprender el modelo si el entrenamiento fuera perfecto**

No responde todavía a:
- si ese aprendizaje se conseguirá
- si convergerá bien
- si generalizará

Eso pertenece a la siguiente sección.

🔗 **Conexión con la sección 6:**  
Una vez definida la capacidad del modelo, la pregunta pasa a ser:

> **cómo se optimizarán sus parámetros durante el entrenamiento**

---

# ⚙️ 6. Configuración del entrenamiento

Esta sección es una de las más críticas, y era justamente una de las que no podía quedar comprimida.

La configuración del entrenamiento define:
- cómo se optimizan los parámetros
- cuán estable es la convergencia
- cuánta señal vs ruido entra en cada actualización
- cómo se gestiona el riesgo de overfitting

## 6.1 Optimizer

| Optimizador | Cuándo suele usarse | Ventaja principal | Riesgo o limitación |
|---|---|---|---|
| Adam | opción por defecto en muchas redes | converge rápido, adapta pasos | no siempre generaliza mejor |
| SGD | cuando interesa control fino o buena generalización | comportamiento más controlado | requiere más tuning |
| RMSprop | problemas secuenciales o alternativa a Adam | adaptación útil en ciertos escenarios | menos universal |
| Adagrad | datos dispersos | útil en sparse features | puede decaer demasiado rápido |

### Lectura conceptual
- **Adam** facilita el arranque y acelera convergencia.
- **SGD** suele exigir más ajuste, pero a veces entrega soluciones más “sobrias”.

## 6.2 Learning rate

El learning rate probablemente sea el hiperparámetro más sensible de todo el entrenamiento.

| Situación observada | Interpretación | Acción razonable |
|---|---|---|
| la pérdida diverge o explota | el paso es demasiado grande | reducir LR |
| la pérdida oscila fuertemente | inestabilidad | reducir LR o batch size / revisar escalado |
| la pérdida baja demasiado lento | el paso es pequeño | aumentar LR |
| el entrenamiento se estanca pronto | puede faltar LR o capacidad | revisar LR y arquitectura |

🔥 **Insight clave:**  
El learning rate no solo controla velocidad. Controla sobre todo **estabilidad**.

## 6.3 Batch size

| Tamaño de batch | Efecto principal | Ventaja | Riesgo |
|---|---|---|---|
| pequeño | gradiente ruidoso | puede generalizar mejor | entrenamiento menos estable o más lento |
| grande | gradiente más estable | mejor uso de hardware | peor generalización en algunos casos |

### Lectura conceptual
El batch size afecta:
- ruido del gradiente
- memoria utilizada
- estabilidad numérica
- velocidad por actualización y por época

## 6.4 Epochs

Las epochs no deberían elegirse como número decorativo.

Deben leerse junto con:
- train loss
- validation loss
- train accuracy
- validation accuracy

| Patrón | Lectura |
|---|---|
| mejora sigue en train y validation | conviene entrenar más |
| mejora train pero validation empeora | aparece overfitting |
| no mejora ni train ni validation | falta capacidad, LR o mejor representación |

## 6.5 Regularización

| Técnica | Función | Cuándo usar |
|---|---|---|
| L2 | penaliza pesos grandes | cuando el modelo se vuelve demasiado sensible |
| Dropout | reduce coadaptación en redes | cuando hay overfitting en redes densas |
| Early stopping | detiene entrenamiento cuando deja de mejorar validación | casi siempre recomendable si hay validación |
| Data augmentation | aumenta variabilidad aparente | especialmente útil en imagen y secuencias |
| Reducción de capacidad | baja complejidad estructural | cuando el modelo memoriza |

## 6.6 Relación entre entrenamiento y arquitectura

La arquitectura define la capacidad potencial.  
El entrenamiento define si esa capacidad:
- converge
- explota
- generaliza
- memoriza

Por eso dos modelos “iguales” en arquitectura pueden comportarse muy distinto si cambian:
- optimizer
- LR
- batch size
- regularización

🔗 **Conexión con la sección 7:**  
Una vez entrenado el modelo, la pregunta no es todavía si “es bueno”, sino:

> **cómo medir su comportamiento de manera adecuada**

---

# 📈 7. Evaluación

La evaluación no puede reducirse a una métrica única.  
Su función es responder, de forma estructurada:

- cuánto falla
- cómo falla
- dónde falla
- si el error observado es aceptable para el problema

## 7.1 Métricas según contexto

| Escenario | Métrica útil | Razón |
|---|---|---|
| clases balanceadas | Accuracy | error global simple |
| clases desbalanceadas | F1 | equilibrio entre precision y recall |
| falsos positivos costosos | Precision | importa evitar positivos incorrectos |
| falsos negativos costosos | Recall | importa no dejar casos verdaderos por fuera |
| regresión sensible a errores grandes | MSE / RMSE | penaliza mucho errores grandes |
| regresión robusta a outliers | MAE | penaliza linealmente |

## 7.2 Curvas de entrenamiento

Observar train y validation permite diagnosticar:

| Patrón en curvas | Diagnóstico probable |
|---|---|
| train bajo y validation bajo | underfitting |
| train muy bueno y validation peor | overfitting |
| oscilación fuerte | inestabilidad de optimización |
| ambos mejoran y se estabilizan cerca | entrenamiento razonable |

## 7.3 Análisis de errores

Herramientas típicas:
- matriz de confusión
- revisión de clases problemáticas
- inspección de ejemplos mal clasificados
- análisis de residuales en regresión

### Idea clave
No basta con saber “cuánto” falla.  
Hay que saber “cómo” falla.

## 7.4 Razón de ser de esta sección

La evaluación convierte el entrenamiento en evidencia.

Pero aún no responde por sí sola:
- por qué ocurre el fallo
- qué debe cambiarse

Eso exige interpretación.

🔗 **Conexión con la sección 8:**  
Una vez medido el comportamiento, la siguiente pregunta es:

> **qué significa ese patrón y qué acción implica**

---

# 🧠 8. Interpretación

Aquí ocurre el Modellvergleich real.  
La interpretación conecta las señales observadas con decisiones concretas.

## 8.1 Diagnóstico → acción

| Problema observado | Acción razonable |
|---|---|
| underfitting | aumentar capacidad, mejorar features, entrenar más |
| overfitting | regularizar, simplificar, usar más datos o early stopping |
| inestabilidad | bajar LR, revisar escalado, ajustar batch |
| mejora marginal de modelo complejo sobre baseline | reconsiderar complejidad |
| gran diferencia entre clases | analizar desbalanceo, features o ruido por clase |

## 8.2 Principio de interpretación

No se interpretan métricas aisladas.  
Se interpretan patrones combinados entre:

- arquitectura
- entrenamiento
- curvas
- métricas
- errores específicos

## 8.3 Preguntas que esta sección debe poder responder

- ¿El modelo complejo mejora de forma real o solo marginal?
- ¿El baseline ya era suficiente?
- ¿La complejidad adicional se justificó?
- ¿El modelo está aprendiendo señal o ruido?
- ¿El error está repartido o concentrado?

🔗 **Conexión con la sección 9:**  
Si la interpretación sugiere que el modelo funciona bien, la siguiente cuestión es:

> **si ese rendimiento puede sostenerse fuera de la muestra observada**

---

# 🌍 9. Generalización

Generalizar significa rendir bien en datos no vistos.

Herramientas principales:
- test set
- validación cruzada
- separación temporal correcta en series
- evaluación externa si existe

## 9.1 Lectura conceptual
Un modelo puede:
- rendir excelente en train
- rendir aceptable en validation
- fallar fuera de muestra

Por eso la generalización no es una propiedad inferida solo desde el train.

## 9.2 Señales útiles
- diferencia moderada y estable entre train y validation
- comportamiento consistente en folds o splits
- degradación aceptable fuera de muestra

---

# ⚠️ 10. Limitaciones

Todo Modellvergleich tiene límites.

Algunos de los más comunes:
- tamaño insuficiente del dataset
- sesgo de muestreo
- ruido no observado
- mala representación de clases minoritarias
- dependencia excesiva de un split concreto
- hiperparámetros ajustados sobre evidencia débil

La utilidad del resultado depende también de reconocer sus límites.

---

# 🧪 11. Errores comunes

- comparar modelos con datasets o splits distintos
- usar solo accuracy
- ignorar el baseline
- cambiar muchas variables a la vez
- concluir demasiado a partir de diferencias pequeñas
- no revisar errores específicos
- no alinear la métrica con el costo real del error
- mezclar familia de modelo, modelo concreto y arquitectura como si fueran lo mismo

---

# 🔁 12. Lógica completa de iteración

El proceso completo no es lineal de una sola pasada.  
Se parece más a un bucle de decisión informado:

```text
problema
   ↓
datos
   ↓
preprocesamiento
   ↓
familia de modelo
   ↓
modelo concreto
   ↓
arquitectura
   ↓
entrenamiento
   ↓
evaluación
   ↓
interpretación
   ↓
ajustes
   ↺
```

## 12.1 Qué cambia cuando el diagnóstico es claro

| Diagnóstico | Tipo de ajuste más razonable |
|---|---|
| underfitting | más capacidad, más epochs, mejores features, cambio de familia |
| overfitting | más regularización, menos capacidad, early stopping, más datos |
| inestabilidad | menor LR, mejor escalado, batch más pequeño o más estable |
| rendimiento ya suficiente con baseline | detener escalada de complejidad |

---

# 📌 Regla final

Si no puede explicarse por qué un modelo funciona mejor que otro,  
no se ha realizado un Modellvergleich; solo se ha ejecutado código.
