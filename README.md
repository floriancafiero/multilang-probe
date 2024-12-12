# multilang-probe

A Python package for analyzing multilingual text.

## Overview

**multilang-probe** is a toolkit designed to classify character sets, detect languages in text files, and extract specific multilingual passages. It supports character detection for a wide range of writing systems using Unicode script properties (e.g., Latin, Japanese, Cyrillic, Arabic, Devanagari, and more). Additionally, it leverages the FastText model for robust language detection.

Whether you are analyzing large corpora or extracting specific language data, **multilang-probe** simplifies the process with an easy-to-use API.

## Features

### Character Set Classification:
- Detect and calculate proportions of character types (e.g., Latin, Japanese, Cyrillic, Arabic, Devanagari) in text.
- Uses `regex` with Unicode script properties (`\p{Script}`) for more accurate classification.
- Special handling for Japanese vs Chinese characters (Han script).

### Language Detection:
- Identify top languages in text using Facebook's FastText pre-trained model.

### Corpus Analysis:
- Detect multilingual passages in large corpora.
- Filter text by specific languages or character sets.
- Extract targeted text based on confidence thresholds.

## Installation

Ensure you have Python >= 3.7 installed.

Clone the repository:
```bash
git clone https://github.com/yourusername/multilang-probe.git
cd multilang-probe
```

Install the package:
```bash
pip install .
```

Install dependencies manually if needed:
```bash
pip install fasttext regex
```

**Note**: The `regex` module is required because the standard `re` module does not support `\p{Script}` properties.

Download the FastText language detection model:
```bash
wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
```

## Usage

### 1. Character Detection
```python
from charlang_detect.character_detection import classify_text_with_proportions

text = "これは日本語と English です。"
proportions = classify_text_with_proportions(text)
print(proportions)
# Possible output:
# {"japanese": 50.0, "latin": 50.0}
```

**Explanation**:  
- If the text contains Hiragana/Katakana, Han characters are considered Japanese Kanji.  
- Otherwise, Han characters are considered Chinese.  
- The output keys may differ from older versions; for example, "cyrillic" instead of "russe", "latin" instead of "latin étendu", etc.

### 2. Language Detection
```python
from charlang_detect.language_detection import detect_language_fasttext

text = "Ceci est un texte en français."
languages = detect_language_fasttext(text)
print(languages)
# Output example: "fr: 99.2%, en: 0.8%"
```

### 3. Corpus Analysis
Analyze all `.txt` files in a folder to detect multilingual passages:
```python
from charlang_detect.corpus_analysis import analyze_corpus_with_fasttext

folder_path = "path/to/corpus/"
results = analyze_corpus_with_fasttext(folder_path)
for filename, langs in results.items():
    print(filename, langs)
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
- Tamil, Bengali, Thai, and many more (extendable via Unicode scripts)
- "other" category for characters not belonging to known scripts

## Dependencies

- Python 3.7+
- FastText
- Regex (for Unicode script classification)

## License

This project is licensed under the MIT License. While the MIT License allows unrestricted use, modification, and distribution of this software, I kindly request that proper credit be given when this project is used in academic, research, or published work. For citation purposes, please refer to the following:

**CAFIERO Florian**, *'multilang-probe'*, 2024, [https://github.com/floriancafiero/multilang-probe].

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## Author

**Florian Cafiero**  
GitHub: [floriancafiero](https://github.com/floriancafiero)  
Email: florian.cafiero@chartes.psl.eu

## Future Features

- Support for other pre-trained language models (e.g., spaCy).
- Visualization tools for multilingual analysis.
- CLI (Command-Line Interface) for easy usage without writing code.
