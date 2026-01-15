import os
from functools import lru_cache
from pathlib import Path

import fasttext

DEFAULT_MODEL_PATH = "lid.176.bin"
ENV_MODEL_PATH = "MULTILANG_PROBE_MODEL_PATH"


@lru_cache(maxsize=1)
def _load_model(model_path):
    path = Path(model_path)
    if not path.is_file():
        raise FileNotFoundError(
            "FastText model not found. Download lid.176.bin or provide a valid path "
            f"via detect_language_fasttext(..., model_path=...) or ${ENV_MODEL_PATH}."
        )
    return fasttext.load_model(str(path))


def detect_language_fasttext(text, k=2, model_path=None):
    # Remplacer les retours à la ligne par des espaces
    resolved_model_path = model_path or os.environ.get(ENV_MODEL_PATH, DEFAULT_MODEL_PATH)
    predictions = _load_model(resolved_model_path).predict(text.replace('\n', ' '), k=k)
    langs = [f"{lang.replace('__label__', '')}: {round(prob * 100, 2)}%"
             for lang, prob in zip(predictions[0], predictions[1])]
    return ", ".join(langs)
