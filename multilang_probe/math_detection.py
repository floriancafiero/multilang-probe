import regex
import unicodedata

MATH_PATTERN = regex.compile(
    r"[\p{Math}\p{Sm}+\-*/=<>^%≈≠≤≥±×÷∑∫√∞∂∆∏∈∉∩∪]"
)


def detect_mathematical_language(text, threshold=1.0):
    normalized_text = unicodedata.normalize("NFC", text)
    non_space_chars = [char for char in normalized_text if not char.isspace()]
    total_characters = len(non_space_chars)
    math_symbols = len(MATH_PATTERN.findall(normalized_text))
    if total_characters == 0:
        return {
            "math_symbols": 0,
            "total_characters": 0,
            "math_ratio": 0.0,
            "is_mathematical": False,
        }
    math_ratio = round((math_symbols / total_characters) * 100, 2)
    return {
        "math_symbols": math_symbols,
        "total_characters": total_characters,
        "math_ratio": math_ratio,
        "is_mathematical": math_ratio >= threshold,
    }
