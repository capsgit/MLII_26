# =========================================================
# PROFILER MODULE
# =========================================================
# Genera un reporte HTML del dataset.
#
# Estrategia:
# 1. Intentar usar ydata-profiling (modo avanzado)
# 2. Si falla -> fallback simple con pandas
# =========================================================

import pandas as pd


# =========================================================
# FUNCIÓN PRINCIPAL
# =========================================================
def build_profile_html(df: pd.DataFrame) -> tuple[str, str]:
    """
    Genera un reporte HTML del DataFrame.

    Returns:
        (html_str, mode)
        mode = "ydata-profiling" | "simple-fallback"
    """

    # -----------------------------------------------------
    # 1) INTENTAR PROFILING AVANZADO
    # -----------------------------------------------------
    try:
        from ydata_profiling import ProfileReport

        report = ProfileReport(
            df,
            title="Data Profile Report",
            explorative=True,
        )

        return report.to_html(), "ydata-profiling"

    except Exception:
        # -------------------------------------------------
        # 2) FALLBACK SIMPLE
        # -------------------------------------------------
        return _build_simple_html(df), "simple-fallback"


# =========================================================
# FALLBACK SIMPLE
# =========================================================
def _build_simple_html(df: pd.DataFrame) -> str:
    """
    Genera un HTML básico con información del dataset.
    """

    # info general
    n_rows, n_cols = df.shape

    # tipos de datos
    dtypes = df.dtypes.to_frame(name="dtype")

    # missing values
    missing = df.isna().sum().to_frame(name="missing_values")

    # stats numéricas
    numeric_summary = df.describe().to_html()

    # stats categóricas (solo si existen)
    categorical_cols = df.select_dtypes(include="object").columns

    if len(categorical_cols) > 0:
        categorical_summary = df[categorical_cols].describe().to_html()
    else:
        categorical_summary = "<p>No categorical columns</p>"

    # construir HTML
    html = f"""
    <html>
        <head>
            <title>Simple Data Profile</title>
        </head>
        <body>
            <h1>Simple Data Profile</h1>

            <h2>Dataset Overview</h2>
            <p>Rows: {n_rows}</p>
            <p>Columns: {n_cols}</p>

            <h2>Data Types</h2>
            {dtypes.to_html()}

            <h2>Missing Values</h2>
            {missing.to_html()}

            <h2>Numeric Summary</h2>
            {numeric_summary}

            <h2>Categorical Summary</h2>
            {categorical_summary}

        </body>
    </html>
    """

    return html