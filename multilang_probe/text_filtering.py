import unicodedata

import regex

from .character_detection import CHARACTER_SETS
from .code_detection import (
    CODE_BLOCK_PATTERN,
    CODE_INLINE_PATTERN,
    CODE_KEYWORD_PATTERN,
    CODE_SYMBOL_PATTERN,
)
from .math_detection import MATH_PATTERN

SCRIPT_ALIASES = {
    **CHARACTER_SETS,
    "hiragana": r"\p{Hiragana}",
    "katakana": r"\p{Katakana}",
    "han": r"\p{Han}",
    "japanese": r"[\p{Hiragana}\p{Katakana}\p{Han}]",
    "chinese": r"\p{Han}",
}


def _compile_script_patterns(scripts):
    if not scripts:
        return {}
    patterns = {}
    for script in scripts:
        script_name = script.strip()
        if not script_name:
            continue
        key = script_name.lower()
        pattern = SCRIPT_ALIASES.get(key)
        if pattern is None:
            pattern = rf"\p{{Script={script_name}}}"
        try:
            patterns[script_name] = regex.compile(pattern)
        except regex.error as exc:
            raise ValueError(f"Unknown or invalid script name: {script_name}") from exc
    return patterns


def _find_code_spans(text):
    spans = []
    for match in CODE_BLOCK_PATTERN.finditer(text):
        spans.append((match.start(), match.end()))
    for match in CODE_INLINE_PATTERN.finditer(text):
        spans.append((match.start(), match.end()))
    for match in CODE_KEYWORD_PATTERN.finditer(text):
        spans.append((match.start(), match.end()))
    return spans


def remove_scripts_and_math(text, scripts=None, remove_math=False, remove_code=False):
    """Remove characters belonging to specified scripts, math symbols, or code tokens."""
    normalized_text = unicodedata.normalize("NFC", text)
    script_patterns = _compile_script_patterns(scripts)
    code_spans = _find_code_spans(normalized_text) if remove_code else []
    span_positions = set()
    for start, end in code_spans:
        span_positions.update(range(start, end))

    if not script_patterns and not remove_math and not remove_code:
        return normalized_text

    filtered_chars = []
    for index, char in enumerate(normalized_text):
        if remove_code and (index in span_positions or CODE_SYMBOL_PATTERN.match(char)):
            continue
        if remove_math and MATH_PATTERN.match(char):
            continue
        if script_patterns and any(pattern.match(char) for pattern in script_patterns.values()):
            continue
        filtered_chars.append(char)
    return "".join(filtered_chars)


def extract_scripts_and_math(
    text, scripts=None, include_math=False, include_code=False, keep_whitespace=True
):
    """Extract characters belonging to specified scripts, math symbols, or code tokens."""
    normalized_text = unicodedata.normalize("NFC", text)
    script_patterns = _compile_script_patterns(scripts)
    code_spans = _find_code_spans(normalized_text) if include_code else []
    span_positions = set()
    for start, end in code_spans:
        span_positions.update(range(start, end))

    if not script_patterns and not include_math and not include_code:
        return ""

    extracted_chars = []
    for index, char in enumerate(normalized_text):
        if keep_whitespace and char.isspace():
            extracted_chars.append(char)
            continue
        if include_code and (index in span_positions or CODE_SYMBOL_PATTERN.match(char)):
            extracted_chars.append(char)
            continue
        if include_math and MATH_PATTERN.match(char):
            extracted_chars.append(char)
            continue
        if script_patterns and any(pattern.match(char) for pattern in script_patterns.values()):
            extracted_chars.append(char)
    return "".join(extracted_chars)
