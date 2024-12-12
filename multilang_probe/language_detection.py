import fasttext

# Assurez-vous que le modèle lid.176.bin se trouve dans le répertoire
# ou fournissez son chemin complet. Vous pouvez le télécharger avant.
MODEL_PATH = "lid.176.bin"
model = fasttext.load_model(MODEL_PATH)

def detect_language_fasttext(text, k=2):
    # Remplacer les retours à la ligne par des espaces
    predictions = model.predict(text.replace('\n', ' '), k=k)
    langs = [f"{lang.replace('__label__', '')}: {round(prob * 100, 2)}%"
             for lang, prob in zip(predictions[0], predictions[1])]
    return ", ".join(langs)
