# multilang-probe

A Python package for analyzing multilingual text.
[![DOI](https://zenodo.org/badge/902241265.svg)](https://doi.org/10.5281/zenodo.14520665)


## Overview

**multilang-probe** is a toolkit designed to classify character sets, detect languages in text files, and extract specific multilingual passages. It supports character detection for a wide range of writing systems using Unicode script properties (e.g., Latin, Japanese, Cyrillic, Arabic, Devanagari, and more). Additionally, it leverages the FastText model for robust language detection. The Zenodo DOI for this release is [10.5281/zenodo.14520665](https://doi.org/10.5281/zenodo.14520665).


## Features

### Character Set Classification:
- Detect and calculate proportions of character types (e.g., Latin, Japanese, Cyrillic, Arabic, Devanagari) in text.
- Uses `regex` with Unicode script properties (`\p{Script}`) for more accurate classification.
- Special handling for Japanese vs Chinese characters (Han script).

#### Example: Character Detection

```python
from multilang_probe.character_detection import classify_text_with_proportions

# Sample text with multiple languages/scripts
text = "これは日本語です。Привет мир! Ελληνικά και हिन्दी।"

# Classify the text
proportions = classify_text_with_proportions(text)

# Print the proportions
print("Character script proportions:")
print(proportions)
```
Expected outcome:

```plaintext
Character script proportions:
{'japanese': 19.51, 'cyrillic': 21.95, 'greek': 26.83, 'devanagari': 14.63, 'other': 17.07}
```


**Explanation**:  
- If the text contains Hiragana/Katakana, Han characters are considered Japanese Kanji.  
- Otherwise, Han characters are considered Chinese.  

### Language Detection:
- Identify top languages in text using Facebook's FastText pre-trained model.
- Install the package from PyPI:

```bash
pip install multilang-probe
```

- Download the model once (example command):

```bash
curl -L -o lid.176.bin https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
```

- Place `lid.176.bin` in your working directory, set `MULTILANG_PROBE_MODEL_PATH`,
  or pass a `model_path` argument (the model file is not bundled with the PyPI package).

#### Example: Language Detection
```python
from multilang_probe.language_detection import detect_language_fasttext

text = "Ceci est un texte en français."
languages = detect_language_fasttext(text, model_path="path/to/lid.176.bin")
print(languages)
# Output example: "fr: 99.2%, en: 0.8%"
```

### Mathematical Language Detection:
- Identify text with a high density of mathematical symbols.

#### Example: Mathematical Detection
```python
from multilang_probe.math_detection import detect_mathematical_language

text = "Let f(x) = ∫_0^∞ e^{-x} dx and x^2 + y^2 = r^2."
result = detect_mathematical_language(text, threshold=1.0)
print(result)
```

### Visualizations:
- Generate simple bar charts for script and language proportions.

#### Example: Script Proportions Plot
```python
from multilang_probe.character_detection import classify_text_with_proportions
from multilang_probe.visualization import plot_script_proportions

text = "これは日本語です。Привет мир!"
proportions = classify_text_with_proportions(text)
plot_script_proportions(proportions, output_path="scripts.png")
```

#### Example: Language Proportions Plot
```python
from multilang_probe.corpus_analysis import analyze_corpus_with_fasttext, calculate_language_proportions
from multilang_probe.visualization import plot_language_proportions

results = analyze_corpus_with_fasttext("path/to/corpus", model_path="path/to/lid.176.bin")
proportions = calculate_language_proportions(results)["example.txt"]
plot_language_proportions(proportions, output_path="languages.png")
```

### Command-Line Interface (CLI)

Install the package and run commands via the `multilang-probe` entry point:

```bash
multilang-probe classify-text --text "これは日本語です。Привет мир!"
```

```bash
multilang-probe detect-language --text "Ceci est un texte en français." --model-path path/to/lid.176.bin
```

```bash
multilang-probe detect-math --text "x^2 + y^2 = r^2" --threshold 1.0
```

```bash
multilang-probe visualize-scripts --text "これは日本語です。Привет мир!" --output scripts.png
```

```bash
multilang-probe visualize-languages --folder path/to/corpus --output languages.png --model-path path/to/lid.176.bin
```

```bash
multilang-probe analyze-corpus --folder path/to/corpus --model-path path/to/lid.176.bin
```

```bash
multilang-probe filter-by-language --folder path/to/corpus --languages fr,en --threshold 70 --model-path path/to/lid.176.bin
```

You can also tune false-positive behavior by aggregating multiple lines into blocks
and enforcing a minimum margin between top-1 and top-2 predictions:

```bash
multilang-probe analyze-corpus \
  --folder path/to/corpus \
  --block-size 3 \
  --min-length 120 \
  --model-path path/to/lid.176.bin
```

```bash
multilang-probe filter-by-language \
  --folder path/to/corpus \
  --languages fr,en \
  --threshold 85 \
  --min-margin 15 \
  --model-path path/to/lid.176.bin
```

### Corpus Analysis:
- Analyze all `.txt` files in a folder to detect multilingual passages and language distributions.
- **Character-based filtering**: Identify and filter text lines containing specific character sets (e.g., Japanese, Cyrillic, Arabic).
- **Language-based filtering**: Extract passages in a specific language, with customizable confidence thresholds (e.g., 70%).
- **Targeted extraction**: Extract lines of text meeting both minimum length requirements and language detection accuracy.
- **Calculate language proportions**: Aggregate detected languages across files and calculate their proportions.

#### Example: Analyze and Detect Multilingual Passages
```python
from multilang_probe.corpus_analysis import analyze_corpus_with_fasttext

folder_path = "path/to/corpus/"
results = analyze_corpus_with_fasttext(folder_path)
for filename, langs in results.items():
    print(filename, langs)
```

#### Example: Filter Passages by Character Types



#### Example: Extract Passages by Language with Threshold
```python
from multilang_probe.corpus_analysis import filter_passages_by_language

folder_path = "path/to/corpus/"
target_languages = ["fr", "en"]
threshold = 70
filtered = filter_passages_by_language(results, target_languages, folder_path, threshold)
for filename, passages in filtered.items():
    print(filename, passages)
```

## Supported Character Sets

- Japanese (Hiragana, Katakana)
- Han (Kanji; considered Japanese if Hiragana/Katakana present, else Chinese)
- Korean (Hangul)
- Cyrillic (for languages like Russian, Bulgarian, etc.)
- Arabic
- Hebrew
- Greek
- Latin (basic and extended)
- Devanagari (e.g., Hindi, Sanskrit)
- Tamil, Bengali, Thai
- Extendable via Unicode scripts
- "other" category for characters not belonging to known scripts

## Dependencies

- Python 3.7+
- FastText
- Matplotlib (for visualizations)
- Regex (for Unicode script classification)

## License

This project is licensed under the MIT License. While the MIT License allows unrestricted use, modification, and distribution of this software, I kindly request that proper credit be given when this project is used in academic, research, or published work. For citation purposes, please refer to the following:

**CAFIERO Florian**, *'multilang-probe'*, 2026, [https://github.com/floriancafiero/multilang-probe].

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## Author

**Florian Cafiero**  
GitHub: [floriancafiero](https://github.com/floriancafiero)  
Email: florian.cafiero@chartes.psl.eu

## Future Features

- Support for other pre-trained language models (e.g., spaCy).
- Support for other languages
- Support for code detection
