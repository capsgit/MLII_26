# models.py
# Mapa de pares (from,to) -> modelo HF MarianMT
# Nota: no todos los pares existen. Si falta, lo añadimos luego.

MODEL_MAP = {
    ("de", "es"): "Helsinki-NLP/opus-mt-de-es",
    ("de", "en"): "Helsinki-NLP/opus-mt-de-en",
    ("de", "fr"): "Helsinki-NLP/opus-mt-de-fr",
    ("de", "it"): "Helsinki-NLP/opus-mt-de-it",
    ("de", "pt"): "Helsinki-NLP/opus-mt-de-pt",
    # Chino: puede existir como -de-zh (depende del repo disponible en HF).
    # Si este nombre fallara, lo ajustamos tras ver el error exacto.
    ("de", "zh"): "Helsinki-NLP/opus-mt-de-zh",
}

LANG_CHOICES = [
    ("Alemán", "de"),
    ("Español", "es"),
    ("Inglés", "en"),
    ("Francés", "fr"),
    ("Italiano", "it"),
    ("Portugués", "pt"),
    ("Chino", "zh"),
]
