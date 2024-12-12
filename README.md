# multilang-probe

**A Python package for analyzing multilingual text.**

---

## **Overview**

`multilang-probe` is a toolkit designed to classify character sets, detect languages in text files, and extract specific multilingual passages. It supports character detection for writing systems like Japanese, Cyrillic, Arabic, and more. Additionally, it leverages the FastText model for robust language detection.

Whether you are analyzing large corpora or extracting specific language data, `multilang-probe` simplifies the process with an easy-to-use API.

---

## **Features**

- **Character Set Classification:**  
   Detect and calculate proportions of character types (e.g., Latin, Japanese, Cyrillic) in text files.

- **Language Detection:**  
   Identify the top languages in text using Facebook's FastText pre-trained model.

- **Corpus Analysis:**  
   - Detect multilingual passages.  
   - Filter text by specific languages or character sets.  
   - Extract targeted text with confidence thresholds.

---

## **Installation**

Ensure you have Python >= 3.7 installed.

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/multilang-probe.git
   cd multilang-probe
   ```

2. Install the package:
   ```bash
   pip install .
   ```

3. Install dependencies manually if needed:
   ```bash
   pip install fasttext regex
   ```

4. Download the **FastText language detection model**:
   ```bash
   wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin
   ```

---

## **Usage**

### **1. Character Detection**

```python
from charlang_detect.character_detection import classify_text_with_proportions

text = "これは日本語と English です。"
proportions = classify_text_with_proportions(text)
print(proportions)
# Output: {'japonais': 62.5, 'latin étendu': 37.5}
```

### **2. Language Detection**

```python
from charlang_detect.language_detection import detect_language_fasttext

text = "Ceci est un texte en français."
languages = detect_language_fasttext(text)
print(languages)
# Output: "fr: 99.2%, en: 0.8%"
```

### **3. Corpus Analysis**

Analyze all `.txt` files in a folder to detect multilingual passages:

```python
from charlang_detect.corpus_analysis import analyze_corpus_with_fasttext

folder_path = "path/to/corpus/"
results = analyze_corpus_with_fasttext(folder_path)
for filename, langs in results.items():
    print(filename, langs)
```

---

## **Supported Character Sets**

- Japanese (Hiragana, Katakana)  
- Kanji (with contextual disambiguation between Chinese and Japanese)
- Cyrillic (Russian, Bulgarian)  
- Arabic  
- Hebrew  
- Greek  
- Latin Extended  
- Other non-ASCII characters  

---

## **Dependencies**

- Python 3.7+  
- [FastText](https://fasttext.cc)  
- Regex  

---

## **License**

This project is licensed under the MIT License. While the MIT License allows unrestricted use, modification, and distribution of this software, I kindly request that proper credit be given when this project is used in academic, research, or published work. For citation purposes, please refer to the following: CAFIERO Florian, 'multilang-probe', 2024, [https://github.com/floriancafiero/multilang-probe].

---

## **Contributing**

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## **Author**

- **Florian Cafiero**  
- GitHub: [floriancafiero](https://github.com/floriancafiero)  
- Email: florian.cafiero@chartes.psl.eu

---

## **Future Features**

- Support for other pre-trained language models (e.g., spaCy).  
- Visualization tools for multilingual analysis.  
- CLI (Command-Line Interface) for easy usage without writing code.
