import regex
import unicodedata

# Dictionary of scripts using Unicode properties (requires the 'regex' module).
# We use \p{Script} or just \p{...} properties to match entire Unicode script ranges.
# You can find a list of valid script names here:
# https://www.unicode.org/standard/supported.html
#
# Note: Adding many scripts can slow down classification slightly, since we
# iterate over them. Consider optimizing if performance is a concern.

CHARACTER_SETS = {
    "japanese_hiragana": r"\p{Hiragana}",
    "japanese_katakana": r"\p{Katakana}",
    "han": r"\p{Han}",                # Chinese characters (also used in Japanese Kanji)
    "korean": r"\p{Hangul}",          # Korean (Hangul)
    "cyrillic": r"\p{Cyrillic}",
    "arabic": r"\p{Arabic}",
    "hebrew": r"\p{Hebrew}",
    "greek": r"\p{Greek}",
    "latin": r"\p{Latin}",
    "devanagari": r"\p{Devanagari}",  # Used by Hindi, Sanskrit, etc.
    "bengali": r"\p{Bengali}",
    "tamil": r"\p{Tamil}",
    "thai": r"\p{Thai}",
    "georgian": r"\p{Georgian}",
    "armenian": r"\p{Armenian}",
    "ethiopic": r"\p{Ethiopic}",
    "gujarati": r"\p{Gujarati}",
    "gurmukhi": r"\p{Gurmukhi}",
    "sinhala": r"\p{Sinhala}",
    "telugu": r"\p{Telugu}",
    "malayalam": r"\p{Malayalam}",
}


def classify_text_with_proportions(text):
    """
    Classify text according to various Unicode scripts and return 
    their proportions in the text.

    Steps:
    1. Normalize the text (NFC) to ensure consistent character representation.
    2. For each character, determine which script category it belongs to.
       If it does not match any known script, categorize it as 'other'.
    3. Special handling for Japanese vs Chinese:
       - If the text contains Hiragana or Katakana, we consider the Han characters as Japanese Kanji.
       - Otherwise, Han characters are considered Chinese.
    4. Calculate the proportions as percentages of total characters.
    """

    normalized_text = unicodedata.normalize('NFC', text)
    total_characters = len(normalized_text)

    char_counts = {charset: 0 for charset in CHARACTER_SETS}
    char_counts["other"] = 0

    # Compile regex patterns for efficiency
    compiled_patterns = {name: regex.compile(pattern) for name, pattern in CHARACTER_SETS.items()}

    # Single pass: For each character, try to match it against each known script
    for char in normalized_text:
        found_category = False
        for charset, pattern in compiled_patterns.items():
            if pattern.match(char):
                char_counts[charset] += 1
                found_category = True
                break
        if not found_category:
            char_counts["other"] += 1

    # Determine if the text is considered Japanese:
    is_japanese = (char_counts["japanese_hiragana"] > 0 or char_counts["japanese_katakana"] > 0)

    final_counts = {}

    # Handle Han characters: Japanese vs Chinese
    if is_japanese:
        japanese_total = (char_counts["japanese_hiragana"] + 
                          char_counts["japanese_katakana"] + 
                          char_counts["han"])
        final_counts["japanese"] = japanese_total
    else:
        if char_counts["han"] > 0:
            final_counts["chinese"] = char_counts["han"]

    # Add other categories that are not Japanese-related
    for charset, count in char_counts.items():
        if charset not in ("japanese_hiragana", "japanese_katakana", "han"):
            if count > 0:
                final_counts[charset] = count

    # Calculate proportions
    proportions = {}
    for charset, count in final_counts.items():
        proportions[charset] = round((count / total_characters) * 100, 2)

    return proportions


if __name__ == "__main__":
    # Example usage: A text with various scripts
    test_text = "これは日本語のテキストです। 한국어 테스트. Кириллица. Ελληνικά. हिन्दी। ქართული (Georgian). Ողջույն (Armenian)."
    result = classify_text_with_proportions(test_text)
    print(result)
