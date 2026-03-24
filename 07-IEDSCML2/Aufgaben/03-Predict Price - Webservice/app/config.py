"""
Paths
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "model_linear_reg_v1.pkl"
DB_PATH = BASE_DIR / "data" / "predictions.db"
