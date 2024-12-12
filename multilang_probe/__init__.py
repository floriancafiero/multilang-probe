try:
    import fasttext
except ImportError:
    raise ImportError(
        "Le module fasttext est requis. Installez-le avec :\n"
        "pip install multilang-probe[fasttext]"
    )
# a voir
