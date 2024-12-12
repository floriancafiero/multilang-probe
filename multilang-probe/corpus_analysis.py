import os
import re
from collections import defaultdict
from .character_detection import CHARACTER_SETS, classify_text_with_proportions
from .language_detection import detect_language_fasttext

def find_texts_with_non_latin_characters(corpus_folder):
    results = {}
    for filename in os.listdir(corpus_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(corpus_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                proportions = classify_text_with_proportions(text)
                if proportions:
                    results[filename] = proportions
    return results

def analyze_corpus_with_fasttext(corpus_folder):
    results = {}
    for filename in os.listdir(corpus_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(corpus_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    text = line.strip()
                    if text:
                        detected_lang = detect_language_fasttext(text)
                        results.setdefault(filename, []).append(detected_lang)
    return results

def calculate_language_proportions(results):
    aggregated_results = {}
    for filename, lang_lines in results.items():
        lang_counts = defaultdict(float)
        for line in lang_lines:
            predictions = [lang_prob.split(": ") for lang_prob in line.split(", ")]
            for lang, prob in predictions:
                lang_counts[lang] += float(prob.strip('%'))
        total = sum(lang_counts.values())
        proportions = {lang: round((count / total) * 100, 2) for lang, count in lang_counts.items()}
        aggregated_results[filename] = proportions
    return aggregated_results

def extract_passages_improved(results, target_language, corpus_folder, threshold=70, min_length=10):
    language_passages = {}
    for filename, lang_lines in results.items():
        file_path = os.path.join(corpus_folder, filename)
        passages = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for idx, line in enumerate(file, start=1):
                text = line.strip()
                if len(text) >= min_length:
                    detected_lang = detect_language_fasttext(text)
                    langs = [lang_prob.split(": ") for lang_prob in detected_lang.split(", ")]
                    for lang, prob in langs:
                        if lang == target_language and float(prob.strip('%')) >= threshold:
                            passages.append((idx, text))
        if passages:
            language_passages[filename] = passages
    return language_passages

def filter_passages_by_character_types(corpus_folder, character_types, min_length=10):
    filtered_passages = {}
    for filename in os.listdir(corpus_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(corpus_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                passages = []
                for idx, line in enumerate(file, start=1):
                    text = line.strip()
                    if len(text) >= min_length:
                        for char_type in character_types:
                            if re.search(CHARACTER_SETS[char_type], text):
                                passages.append((idx, text))
                                break
            if passages:
                filtered_passages[filename] = passages
    return filtered_passages

def filter_passages_by_language(results, target_languages, corpus_folder, threshold=70, min_length=10):
    filtered_passages = {}
    for filename, lang_lines in results.items():
        file_path = os.path.join(corpus_folder, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            passages = []
            for idx, line in enumerate(file, start=1):
                text = line.strip()
                if len(text) >= min_length:
                    detected_lang = detect_language_fasttext(text)
                    langs = [lang_prob.split(": ") for lang_prob in detected_lang.split(", ")]
                    for lang, prob in langs:
                        if lang in target_languages and float(prob.strip('%')) >= threshold:
                            passages.append((idx, text))
                            break
            if passages:
                filtered_passages[filename] = passages
    return filtered_passages
