# Data Cleaning Pipeline

## 🎯 Purpose

This project implements a configurable and reproducible data cleaning pipeline.

The goal is NOT machine learning yet.
The goal is to:

- Load raw CSV data
- Apply ordered cleaning steps defined in a JSON file
- Log transformations
- Output a cleaned dataset

The pipeline is fully controlled via configuration.

---

## 🧠 Conceptual Architecture

The project separates responsibilities:

| Layer | Responsibility |
|-------|---------------|
| JSON config | Defines WHAT cleaning steps to execute |
| DataCleaner | Implements HOW steps are executed |
| Runner script | Orchestrates execution |
| Logs | Provide traceability |

---

## 🔁 High-Level Flow

```text
Run script
    ↓
Load config
    ↓
Read raw CSV
    ↓
Execute cleaning steps in order
    ↓
Log row changes
    ↓
Save cleaned CSV