import regex
import unicodedata

CODE_SYMBOL_PATTERN = regex.compile(r"[{}()[\];,.:=<>/*+\-_|#@`$%^&~]")
CODE_KEYWORD_PATTERN = regex.compile(
    r"\b("
    r"def|class|return|import|from|as|with|lambda|yield|async|await|try|except|finally|"
    r"if|elif|else|for|while|break|continue|pass|raise|"
    r"function|const|let|var|new|this|switch|case|default|"
    r"library|require|pkg|data|model|plot|ggplot|"
    r"SELECT|FROM|WHERE|INSERT|UPDATE|DELETE"
    r")\b",
    flags=regex.IGNORECASE,
)
CODE_BLOCK_PATTERN = regex.compile(r"```.*?```", flags=regex.DOTALL)
CODE_INLINE_PATTERN = regex.compile(r"`[^`]+`")


def detect_code_like_language(text, threshold=1.0):
    normalized_text = unicodedata.normalize("NFC", text)
    non_space_chars = [char for char in normalized_text if not char.isspace()]
    total_characters = len(non_space_chars)
    if total_characters == 0:
        return {
            "code_symbols": 0,
            "keyword_matches": 0,
            "total_characters": 0,
            "code_ratio": 0.0,
            "is_code_like": False,
        }

    code_symbols = len(CODE_SYMBOL_PATTERN.findall(normalized_text))
    keyword_matches = len(CODE_KEYWORD_PATTERN.findall(normalized_text))
    code_ratio = round((code_symbols / total_characters) * 100, 2)
    return {
        "code_symbols": code_symbols,
        "keyword_matches": keyword_matches,
        "total_characters": total_characters,
        "code_ratio": code_ratio,
        "is_code_like": code_ratio >= threshold or keyword_matches > 0,
    }
