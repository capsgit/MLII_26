# ------------------------------------------------------------
# DataCleaner = “motor” de limpieza configurable por JSON.
#
# Idea:
#   - El JSON decide QUÉ pasos se ejecutan y en QUÉ orden.
#   - Este archivo implementa CÓMO se ejecuta cada paso.
#   - El logger deja evidencia (auditable) de cuántas filas cambian por step.
#
# Flujo mental:
#   DataCleaner(config_path)
#       -> carga config
#       -> construye logger
#       -> clean_data()
#             1) lee CSV
#             2) ejecuta steps en orden
#             3) guarda CSV limpio
#             4) devuelve df limpio
#
#
#
# ------------------------------------------------------------
# class DataCleaner:
#   def __init__(self, config_path):
#      with open(config_path) as f:
#          self.config = json.load(f)
#
#   def clean_data(self):
#      df = pd.read_csv(self.config["input_path"])
#
#       for step in self.config["steps"]:
#          if step["name"] == "drop_empty_rows":
#             df = df.dropna(how="all")
#
#       df.to_csv(self.config["output_path"], index=False)
#      return df
# ------------------------------------------------------------

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass
class DataCleaner:
    """
    Clase encargada de:
      - Leer un JSON de configuración
      - Ejecutar un pipeline de cleaning (lista de 'steps')
      - Escribir logs y guardar el dataset limpio

    NOTA: aquí NO definimos target ni creamos X/y.
          Solo dejamos el dataframe "sano" y reproducible.
    """
    config_path: str

    # se ejecuta justo despues del __init__
    def __post_init__(self) -> None:
        # ----------------------------------------------------
        # para arreglar los paths relativos:
        #
        # import os
        #
        # from pathlib import Path
        #
        # os.chdir(Path(__file__).parent))
        # -----------------------------------------------------

        # project_root apunta a la carpeta raíz del proyecto:
        #   .../Data Cleaning/
        # Porque este archivo vive en:
        #   .../Data Cleaning/src/data_cleaner.py
        # parents[1] => sube de src/ a la raíz del proyecto
        self.project_root = Path(__file__).resolve().parents[1]

        # Cargar config desde JSON (contrato del pipeline)
        self.config = self._load_config(self.config_path)

        # Construir logger: escribe a archivo y también a consola
        self.logger = self._build_logger(self.config.get("log_path", "logs/cleaning.log"))

    def _load_config(self, config_path: str) -> dict:
        """
        Carga el JSON de configuración.

        Pseudocódigo:
            cfg_path = project_root + config_path
            si no existe -> error (mejor fallar temprano)
            return json.load(cfg_path)
        """
        cfg_path = (self.project_root / config_path).resolve()
        if not cfg_path.exists():
            raise FileNotFoundError(f"Config not found: {cfg_path}")

        with open(cfg_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _build_logger(self, log_path: str) -> logging.Logger:
        """
        Construye un logger con:
          - FileHandler: logs/cleaning.log
          - StreamHandler: consola

        Pseudocódigo:
            logger = getLogger("data_cleaner")
            si ya tiene handlers -> no duplicar
            crear carpeta logs/
            crear formato
            conectar handlers
        """
        logger = logging.getLogger("data_cleaner")
        logger.setLevel(logging.INFO)

        # Si corres esto varias veces dentro del mismo intérprete (ej. notebook),
        # evita agregar handlers repetidos (si no, verías logs duplicados).
        if logger.handlers:
            return logger

        log_file = (self.project_root / log_path).resolve()
        log_file.parent.mkdir(parents=True, exist_ok=True)

        log_format = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

        # Handler A: archivo - fh ------------------------------------
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(log_format)
        fh.setLevel(logging.INFO)

        # Handler B: consola - sh ------------------------------------
        sh = logging.StreamHandler()
        sh.setFormatter(log_format)
        sh.setLevel(logging.INFO)

        logger.addHandler(fh)
        logger.addHandler(sh)
        return logger

    def clean_data(self) -> pd.DataFrame:
        """
        Ejecuta el pipeline de cleaning definido por el JSON.
        """
        # ----------------------------------------------------
        #   df = pd.read_csv(input_path)
        #   for step in config["steps"]:
        #       aplicar_transformacion(df)
        #   df.to_csv(output_path)
        #   return df
        # ----------------------------------------------------
        # para arreglar los paths relativos:
        #
        # import os
        #
        # from pathlib import Path
        #
        # os.chdir(Path(__file__).parent))
        # -----------------------------------------------------

        input_path = (self.project_root / self.config["input_path"]).resolve()
        output_path = (self.project_root / self.config["output_path"]).resolve()

        if not input_path.exists():
            raise FileNotFoundError(f"Input CSV not found: {input_path}")

        self.logger.info(f"Reading: {input_path}")
        df = pd.read_csv(input_path)

        self.logger.info(f"Columns: {list(df.columns)}")
        self.logger.info(f"Rows in: {len(df)}")

        steps = self.config.get("steps", [])
        if not steps:
            self.logger.warning("No steps found in config. Returning raw dataframe.")

        # Ejecutar cada step en orden (el orden importa)
        for i, step in enumerate(steps, start=1):
            name = step.get("name")
            if not name:
                raise ValueError(f"Step #{i} has no 'name': {step}")

            before = len(df)

            # STEP 1: eliminar filas completamente vacías
            if name == "drop_empty_rows":
                df = df.dropna(how="all")

            # STEP 2: eliminar filas que son un header repetido dentro del dataset
            # (En datasets de ventas tipo Kaggle, ocurre a veces.)
            elif name == "remove_repeated_header_rows":
                col = step["column"]
                header_value = step["header_value"]
                if col in df.columns:
                    df = df[df[col].astype(str) != header_value]
                else:
                    self.logger.warning(f"{name}: column '{col}' not found; skipped")

            # STEP 3: castear columnas a numérico (si no se puede convertir -> NaN)
            elif name == "cast_numeric":
                cols = step["columns"]
                for c in cols:
                    if c in df.columns:
                        df[c] = pd.to_numeric(df[c], errors="coerce")
                    else:
                        self.logger.warning(f"{name}: column '{c}' not found; skipped")

            # STEP 4: castear una columna a datetime (si no se puede -> NaT)
            elif name == "cast_datetime":
                c = step["column"]
                if c in df.columns:
                    df[c] = pd.to_datetime(df[c], format="%m/%d/%y %H:%M", errors="coerce")
                else:
                    self.logger.warning(f"{name}: column '{c}' not found; skipped")

            # STEP 5: eliminar filas con NaN/NaT después de los casts
            # (es "estricto": quita filas con cualquier NA en cualquier columna)
            elif name == "drop_na_after_cast":
                df = df.dropna()

            # STEP 6: eliminar duplicados exactos
            elif name == "drop_duplicates":
                df = df.drop_duplicates()

            else:
                raise ValueError(f"Unknown step: {name}")

            after = len(df)
            self.logger.info(f"[{i}/{len(steps)}] {name}: {before} -> {after} (removed {before - after})")

        # Guardar resultado final
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        self.logger.info(f"Saved: {output_path}")
        self.logger.info(f"Rows out: {len(df)}")
        return df