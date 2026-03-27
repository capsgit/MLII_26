# 🎓 Training Repository
## Overview

Este repositorio documenta el progreso práctico dentro del programa:

#  Python Data Certified Associate (WBS Training)

El contenido cubre un recorrido completo desde fundamentos de programación hasta Machine Learning, Deep Learning y Data Engineering, incluyendo también:

- Desarrollo de software en Python
- Bases de datos (SQL / NoSQL)
- Interfaces gráficas (GUI)
- APIs y pipelines de datos
- Cloud aplicado a Data Science

No es un proyecto único, sino un workspace estructurado por módulos, donde cada carpeta representa una fase del aprendizaje.

---
## 🎯 Objetivo del repositorio
- Consolidar conocimientos mediante práctica
- Construir piezas reutilizables (scripts, mini-proyectos) 
- Entender el ciclo completo de datos:
    ```markdown
    Data → Processing → Modeling → Evaluation → Deployment
    ```
- Servir como base para proyectos más complejos (ML APIs, pipelines, productos data-driven)
---
## 📁 Estructura del proyecto
```
MLII_26/
│
├── 02-IEPYTPP        # Fundamentos Python (tipos, control, funciones)
├── 03-IEPYTFM        # Estructuras, modularización, buenas prácticas
├── 04-IEDSCDB        # Bases de datos (SQL, SQLite, NoSQL)
├── 05-IEPYTUI        # Interfaces gráficas (Tkinter / UI)
├── 06-IEDSCML1       # Machine Learning (fundamentos)
├── 07-IEDSCML2       # ML avanzado / pipelines / evaluación
├── 08-IEDSCNN        # Deep Learning (CNN, TensorFlow)
│
├── sonstiges/        # Proyectos complementarios
│   ├── Traductor     # NLP + GUI
│   ├── Notepad       # Manejo de archivos / UI
│   ├── Juego Sudoku  # Lógica + estructuras
│   └── Juego Ahorcado
│
├── main.py
├── meine_daten.xlsx
├── solutions.db
├── requirements.txt
└── README.md
```
---
## 🧩 Módulos de aprendizaje

---
### 🐍 Python & Software Engineering
- Tipos de datos y estructuras
- Control de flujo
- Funciones y modularización
- Namespaces y side effects
- Buenas prácticas de código

👉 Aquí se construye la base para todo lo demás.

---

### 🗄️ Bases de Datos (SQL / NoSQL)
- Modelado relacional
- Queries con SQL
- Uso de SQLite/MySQL
- Introducción a NoSQL

👉 **En el repo:**

- ```solutions.db``` → almacenamiento estructurado
- Scripts de acceso a datos

---
### 🖥️ Interfaces Gráficas (GUI)
- Tkinter / widgets
- Layouts y eventos
- Aplicaciones desktop simples

**👉 Ejemplo:**

- Traductor de notebooks
- Notepad custom

---
### 📈 Machine Learning I & II
- Estadística aplicada
- Vectores, matrices, datasets
- Modelos clásicos:
  + KNN
  + SVM
  + Regresión
- Pipelines de ML
- Evaluación de modelos

👉 Flujo típico aplicado en el repo:

```
Load → Clean → Transform → Train → Evaluate
```
---
### 🧠 Deep Learning
- Redes neuronales
- TensorFlow / Keras
- MNIST (clasificación de imágenes)
- Arquitecturas básicas:
  + Dense
  + Conv2D
  + Pooling
  + Dropout

---
### 🔄 Data Engineering & APIs
- ETL procesos
- REST APIs
- Data pipelines
- Integración de servicios

👉 Esto conecta ML con sistemas reales.

---
### ☁️ Cloud & Deployment
- Conceptos cloud
- Servicios de datos
- ML en la nube
- Integración de modelos en sistemas productivos

---
## ⚙️ Setup

``` bash
    git clone https://github.com/capsgit/MLII_26.git
    cd MLII_26
    python -m venv .venv
```

Activar entorno:
``` bash    
    # Windows
    .venv\Scripts\activate
    
    # Linux / Mac
    source .venv/bin/activate
```
Instalar dependencias:
``` bash
    pip install -r requirements.txt
```
---
## 🚀 Uso

Dependiendo del módulo:

Ejecutar scripts
```bash
  python main.py
```
Trabajar con notebooks

Recomendado en:

* Jupyter
* VS Code
* PyCharm

---
## 🚠 Enfoque técnico del repositorio

Este repo refleja una transición clara:

#### 1. Programación

    → lógica, estructuras, funciones

#### 2. Datos

    → bases de datos, limpieza, transformación

#### 3. Modelos

    → ML + DL

#### 4. Sistemas

    → APIs, pipelines, cloud

---
## 📊 Evaluación de modelos

Se usan métricas como:

  - Accuracy
  - Confusion Matrix
  - Precision / Recall

### ⚠️ Importante:

Un modelo puede “verse mejor” (gráficas, training curves)
pero **no necesariamente generaliza mejor**.

👉 Por eso se comparan múltiples métricas.

---


# ⛳ Proyectos destacados

## 🌐 Traductor (NLP + GUI)
- Procesamiento de texto
- Interfaz gráfica
- Integración de modelos

## ✈️ Flight / Data projects (si los integras luego)
- ETL
- API consumption
- almacenamiento en DB

---
# 🗃️ Buenas prácticas trabajadas
- Separación por módulos
- Uso de entornos virtuales
- Persistencia con SQLite
- Estructuración progresiva del código
- Introducción a pipelines de datos


# 📬 Contact

GitHub: https://github.com/capsgit