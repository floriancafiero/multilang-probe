import os
import re
from collections import defaultdict
from .character_detection import CHARACTER_SETS, classify_text_with_proportions
from .language_detection import detect_language_fasttext, detect_language_fasttext_with_probs

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

def analyze_corpus_with_fasttext(corpus_folder, k=2, model_path=None, min_length=1, block_size=1):
    results = {}
    for filename in os.listdir(corpus_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(corpus_folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                buffer = []
                for line in file:
                    text = line.strip()
                    if not text:
                        continue
                    buffer.append(text)
                    if len(buffer) >= block_size:
                        block = " ".join(buffer)
                        buffer = []
                        if len(block) >= min_length:
                            detected_lang = detect_language_fasttext(
                                block, k=k, model_path=model_path
                            )
                            results.setdefault(filename, []).append(detected_lang)
                if buffer:
                    block = " ".join(buffer)
                    if len(block) >= min_length:
                        detected_lang = detect_language_fasttext(
                            block, k=k, model_path=model_path
                        )
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

def extract_passages_improved(
    results,
    target_language,
    corpus_folder,
    threshold=70,
    min_margin=0,
    min_length=10,
    k=2,
    model_path=None,
):
    language_passages = {}
    for filename, lang_lines in results.items():
        file_path = os.path.join(corpus_folder, filename)
        passages = []
        with open(file_path, 'r', encoding='utf-8') as file:
            for idx, line in enumerate(file, start=1):
                text = line.strip()
                if len(text) >= min_length:
                    k_for_margin = max(k, 2) if min_margin else k
                    langs = detect_language_fasttext_with_probs(
                        text, k=k_for_margin, model_path=model_path
                    )
                    if not langs:
                        continue
                    top_lang, top_prob = langs[0]
                    second_prob = langs[1][1] if len(langs) > 1 else 0
                    if min_margin and top_lang != target_language:
                        continue
                    if min_margin and (top_prob - second_prob) < min_margin:
                        continue
                    for lang, prob in langs:
                        if lang == target_language and prob >= threshold:
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

def filter_passages_by_language(
    results,
    target_languages,
    corpus_folder,
    threshold=70,
    min_margin=0,
    min_length=10,
    k=2,
    model_path=None,
):
    filtered_passages = {}
    for filename, lang_lines in results.items():
        file_path = os.path.join(corpus_folder, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            passages = []
            for idx, line in enumerate(file, start=1):
                text = line.strip()
                if len(text) >= min_length:
                    k_for_margin = max(k, 2) if min_margin else k
                    langs = detect_language_fasttext_with_probs(
                        text, k=k_for_margin, model_path=model_path
                    )
                    if not langs:
                        continue
                    top_lang, top_prob = langs[0]
                    second_prob = langs[1][1] if len(langs) > 1 else 0
                    if min_margin and top_lang not in target_languages:
                        continue
                    if min_margin and (top_prob - second_prob) < min_margin:
                        continue
                    for lang, prob in langs:
                        if lang in target_languages and prob >= threshold:
                            passages.append((idx, text))
                            break
            if passages:
                filtered_passages[filename] = passages
    return filtered_passages
