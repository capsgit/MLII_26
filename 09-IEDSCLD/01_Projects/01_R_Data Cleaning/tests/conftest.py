# =========================================================
# CONFIG GLOBAL PARA TESTS
# =========================================================
# Esto añade la carpeta raíz al path de Python
# para que "src" sea importable
# =========================================================

import sys
from pathlib import Path

# ruta del proyecto (una carpeta arriba de tests/)
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# añadir al sys.path
sys.path.append(str(PROJECT_ROOT))