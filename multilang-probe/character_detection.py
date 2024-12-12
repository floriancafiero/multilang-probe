import re
import unicodedata

CHARACTER_SETS = {
    "japonais": r'[\u3040-\u309F\u30A0-\u30FF\u31F0-\u31FF]',
    "kanji": r'[\u4E00-\u9FFF]',
    "coréen": r'[\uAC00-\uD7AF\u1100-\u11FF]',
    "russe": r'[\u0400-\u04FF]',
    "arabe": r'[\u0600-\u06FF\u0750-\u077F]',
    "hébreu": r'[\u0590-\u05FF]',
    "grec": r'[\u0370-\u03FF]',
    "latin étendu": r'[\u0100-\u024F]',
    "autre": r'[^\u0000-\u007F]',
}

def classify_text_with_proportions(text):
    normalized_text = unicodedata.normalize('NFC', text)
    total_characters = len(normalized_text)
    char_counts = {charset: 0 for charset in CHARACTER_SETS}

    # Compter les caractères pour chaque ensemble
    for charset, regex in CHARACTER_SETS.items():
        char_counts[charset] += len(re.findall(regex, normalized_text))

    # Traitement spécifique pour japonais et chinois
    is_japanese = char_counts["japonais"] > 0
    has_kanji = char_counts["kanji"] > 0

    if is_japanese:
        char_counts["japonais"] += char_counts["kanji"]
        char_counts["kanji"] = 0
    elif has_kanji:
        # Ajouter une catégorie chinoise si nécessaire
        char_counts["chinois"] = char_counts["kanji"]
        char_counts["kanji"] = 0

    # Calculer les proportions en pourcentage
    proportions = {}
    for charset, count in char_counts.items():
        if count > 0:
            proportions[charset] = round((count / total_characters) * 100, 2)

    return proportions
