# =========================================================
# TESTS PARA cleaner.py
# =========================================================
# Idea:
# - probar el flujo completo
# - no cada función aislada (eso ya está en test_steps)
# =========================================================

import pandas as pd

from src.cleaning.cleaner import DataCleaner
from src.cleaning.options import CleaningOptions
from src.utils.logger import build_logger


# ---------------------------------------------------------
# helper: crear cleaner
# ---------------------------------------------------------
def get_cleaner():
    logger = build_logger("test_logger")
    return DataCleaner(logger=logger)


# ---------------------------------------------------------
# TEST 1: pipeline básico
# ---------------------------------------------------------
# Pseudocódigo:
# activar drop_empty_rows
# verificar que elimina filas vacías
# ---------------------------------------------------------
def test_cleaner_removes_empty_rows():
    cleaner = get_cleaner()

    df = pd.DataFrame({
        "A": [1, None],
        "B": [2, None],
    })

    options = CleaningOptions(
        drop_empty_rows=True
    )

    result = cleaner.clean_dataframe(df, options)

    assert result.rows_after == 1


# ---------------------------------------------------------
# TEST 2: sin pasos activados
# ---------------------------------------------------------
# Pseudocódigo:
# no activar nada
# resultado debe ser igual al input
# ---------------------------------------------------------
def test_cleaner_without_steps_returns_same_dataframe():
    cleaner = get_cleaner()

    df = pd.DataFrame({
        "A": [1, 2]
    })

    options = CleaningOptions()

    result = cleaner.clean_dataframe(df, options)

    assert result.rows_before == result.rows_after


# ---------------------------------------------------------
# TEST 3: cast_numeric dentro del pipeline
# ---------------------------------------------------------
def test_cleaner_cast_numeric_step():
    cleaner = get_cleaner()

    df = pd.DataFrame({
        "price": ["10", "abc"]
    })

    options = CleaningOptions(
        cast_numeric=True,
        numeric_columns=["price"]
    )

    result = cleaner.clean_dataframe(df, options)

    assert result.cleaned_df["price"].isna().sum() == 1


# ---------------------------------------------------------
# TEST 4: applied_steps se llena
# ---------------------------------------------------------
def test_cleaner_applied_steps_is_not_empty():
    cleaner = get_cleaner()

    df = pd.DataFrame({
        "A": [1, None],
        "B": [2, None],
    })

    options = CleaningOptions(
        drop_empty_rows=True
    )

    result = cleaner.clean_dataframe(df, options)

    assert len(result.applied_steps) > 0