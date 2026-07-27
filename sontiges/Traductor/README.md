# 🌍 AI Notebook Translator

A Python application that automatically translates Jupyter Notebooks while preserving their complete notebook structure and source code.

Instead of translating plain text files, the application understands the internal JSON structure of `.ipynb` notebooks, identifies Markdown cells, translates only human-readable content using an AI translation model, and generates a fully functional translated notebook.

---

# 📌 Business Problem

Technical courses frequently consist of dozens of Jupyter Notebooks written in a single language.

Manually translating each notebook is repetitive, time-consuming and error-prone. Furthermore, translating notebooks with conventional translation tools often breaks formatting or modifies code cells.

This project automates that process while preserving the technical integrity of the notebooks.

---

# 🎯 Solution

The application automatically:

- reads Jupyter Notebook files (`.ipynb`)
- parses the notebook JSON structure
- detects Markdown cells
- keeps code cells completely untouched
- translates Markdown content using an AI language model
- rebuilds a valid translated notebook

The result is a notebook that can be opened immediately in Jupyter without any manual corrections.

---

# ⚙️ Workflow

```

Jupyter Notebook
   ↓
Read JSON
   ↓
Detect Markdown Cells
   ↓
AI Translation
   ↓
Rebuild Notebook
   ↓
Translated Notebook

```

---

# ✨ Features

- Automatic notebook parsing
- AI-powered translation
- Markdown detection
- Code preservation
- Notebook reconstruction
- Batch processing support
- Multi-language user interface
- Progress indication

---

# 🧠 Design Philosophy

The project was designed around one central principle:

> Preserve everything that belongs to the notebook except the natural language.

For that reason the application never translates:

- Python code
- outputs
- notebook metadata
- execution information

Only the Markdown documentation is modified.

---

# 📂 Project Structure

```

Translator/

│
├── gui.py                 # User Interface
├── engine.py              # Translation Engine
├── models.py              # AI Model Management
├── translator.py          # Translation Logic
├── utils.py
│
└── notebooks/

```

---

# 🛠 Technologies

Python

Transformers (Hugging Face)

MarianMT

PyTorch

Tkinter

JSON

Jupyter Notebook Format

---

# ▶️ Installation

### Create virtual environment

```bash
python -m venv .venv
```

### Activate

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

# 🚀 Run

```bash
python gui.py
```

---

# 💻 Usage

1. Select one or more Jupyter Notebooks.
2. Choose the target language.
3. Start the translation.
4. The translated notebook is automatically generated.

---

# 📈 Business Value

The application significantly reduces the manual effort required to translate technical learning material.

It enables:

- reuse of educational content
- multilingual documentation
- consistent notebook structure
- scalable translation workflows

---

# 🚀 Possible Improvements

- Support additional translation models
- Automatic language detection
- Cloud translation providers
- Translation memory
- Quality evaluation metrics
- CLI mode
- Docker deployment

---

# 📄 License

Educational project.