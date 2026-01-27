import argparse
import json
import sys
from pathlib import Path

from .character_detection import classify_text_with_proportions
from .corpus_analysis import (
    analyze_corpus_with_fasttext,
    calculate_language_proportions,
    extract_passages_improved,
    filter_passages_by_character_types,
    filter_passages_by_language,
)
from .language_detection import detect_language_fasttext
from .code_detection import detect_code_like_language
from .math_detection import detect_mathematical_language
from .text_filtering import extract_scripts_and_math, remove_scripts_and_math
from .visualization import plot_language_proportions, plot_script_proportions


def _load_text(text, file_path):
    if text:
        return text
    if file_path:
        return Path(file_path).read_text(encoding="utf-8")
    return sys.stdin.read()


def _print_json(payload):
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def _aggregate_language_proportions(results):
    aggregated = {}
    for lang_lines in results.values():
        for line in lang_lines:
            predictions = [lang_prob.split(": ") for lang_prob in line.split(", ")]
            for lang, prob in predictions:
                aggregated[lang] = aggregated.get(lang, 0) + float(prob.strip("%"))
    total = sum(aggregated.values())
    if total == 0:
        return {}
    return {lang: round((count / total) * 100, 2) for lang, count in aggregated.items()}


def build_parser():
    parser = argparse.ArgumentParser(
        description="CLI utilities for the multilang-probe toolkit."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    classify_parser = subparsers.add_parser(
        "classify-text", help="Classify text by Unicode script proportions."
    )
    classify_parser.add_argument("--text", help="Text to classify.")
    classify_parser.add_argument("--file", help="Path to a UTF-8 text file.")

    detect_parser = subparsers.add_parser(
        "detect-language", help="Detect languages using FastText."
    )
    detect_parser.add_argument("--text", help="Text to analyze.")
    detect_parser.add_argument("--file", help="Path to a UTF-8 text file.")
    detect_parser.add_argument("--k", type=int, default=2, help="Top-k languages.")
    detect_parser.add_argument(
        "--model-path", help="Path to lid.176.bin (or set MULTILANG_PROBE_MODEL_PATH)."
    )

    math_parser = subparsers.add_parser(
        "detect-math", help="Detect mathematical language based on symbol density."
    )
    math_parser.add_argument("--text", help="Text to analyze.")
    math_parser.add_argument("--file", help="Path to a UTF-8 text file.")
    math_parser.add_argument(
        "--threshold",
        type=float,
        default=1.0,
        help="Threshold percentage to flag mathematical language.",
    )

    code_parser = subparsers.add_parser(
        "detect-code", help="Detect code-like language based on symbol density."
    )
    code_parser.add_argument("--text", help="Text to analyze.")
    code_parser.add_argument("--file", help="Path to a UTF-8 text file.")
    code_parser.add_argument(
        "--threshold",
        type=float,
        default=1.0,
        help="Threshold percentage to flag code-like language.",
    )

    visualize_scripts_parser = subparsers.add_parser(
        "visualize-scripts",
        help="Plot script proportions for a text input.",
    )
    visualize_scripts_parser.add_argument("--text", help="Text to analyze.")
    visualize_scripts_parser.add_argument("--file", help="Path to a UTF-8 text file.")
    visualize_scripts_parser.add_argument(
        "--output",
        help="Output image path (e.g., scripts.png). If omitted, shows the plot.",
    )
    visualize_scripts_parser.add_argument("--title", help="Plot title.")

    visualize_languages_parser = subparsers.add_parser(
        "visualize-languages",
        help="Plot language proportions for a corpus.",
    )
    visualize_languages_parser.add_argument(
        "--folder", required=True, help="Corpus folder path."
    )
    visualize_languages_parser.add_argument(
        "--file",
        help="Optional filename in the corpus to visualize. Defaults to aggregate.",
    )
    visualize_languages_parser.add_argument(
        "--output",
        help="Output image path (e.g., languages.png). If omitted, shows the plot.",
    )
    visualize_languages_parser.add_argument("--title", help="Plot title.")
    visualize_languages_parser.add_argument("--k", type=int, default=2, help="Top-k languages.")
    visualize_languages_parser.add_argument(
        "--min-length",
        type=int,
        default=1,
        help="Minimum block length for language detection.",
    )
    visualize_languages_parser.add_argument(
        "--block-size",
        type=int,
        default=1,
        help="Number of non-empty lines to merge per detection.",
    )
    visualize_languages_parser.add_argument(
        "--model-path", help="Path to lid.176.bin (or set MULTILANG_PROBE_MODEL_PATH)."
    )

    corpus_parser = subparsers.add_parser(
        "analyze-corpus", help="Analyze a folder of .txt files with FastText."
    )
    corpus_parser.add_argument("--folder", required=True, help="Corpus folder path.")
    corpus_parser.add_argument("--k", type=int, default=2, help="Top-k languages.")
    corpus_parser.add_argument(
        "--min-length",
        type=int,
        default=1,
        help="Minimum block length for language detection.",
    )
    corpus_parser.add_argument(
        "--block-size",
        type=int,
        default=1,
        help="Number of non-empty lines to merge per detection.",
    )
    corpus_parser.add_argument(
        "--model-path", help="Path to lid.176.bin (or set MULTILANG_PROBE_MODEL_PATH)."
    )

    proportions_parser = subparsers.add_parser(
        "language-proportions",
        help="Aggregate language proportions across a corpus.",
    )
    proportions_parser.add_argument("--folder", required=True, help="Corpus folder path.")
    proportions_parser.add_argument("--k", type=int, default=2, help="Top-k languages.")
    proportions_parser.add_argument(
        "--min-length",
        type=int,
        default=1,
        help="Minimum block length for language detection.",
    )
    proportions_parser.add_argument(
        "--block-size",
        type=int,
        default=1,
        help="Number of non-empty lines to merge per detection.",
    )
    proportions_parser.add_argument(
        "--model-path", help="Path to lid.176.bin (or set MULTILANG_PROBE_MODEL_PATH)."
    )

    filter_chars_parser = subparsers.add_parser(
        "filter-by-characters", help="Extract passages containing character types."
    )
    filter_chars_parser.add_argument("--folder", required=True, help="Corpus folder path.")
    filter_chars_parser.add_argument(
        "--types",
        required=True,
        help="Comma-separated list of character types (e.g., japanese, cyrillic).",
    )
    filter_chars_parser.add_argument(
        "--min-length", type=int, default=10, help="Minimum line length."
    )

    filter_lang_parser = subparsers.add_parser(
        "filter-by-language", help="Extract passages matching target languages."
    )
    filter_lang_parser.add_argument("--folder", required=True, help="Corpus folder path.")
    filter_lang_parser.add_argument(
        "--languages",
        required=True,
        help="Comma-separated list of language codes (e.g., fr,en).",
    )
    filter_lang_parser.add_argument(
        "--threshold", type=float, default=70, help="Confidence threshold (0-100)."
    )
    filter_lang_parser.add_argument(
        "--min-margin",
        type=float,
        default=0,
        help="Minimum probability margin between top-1 and top-2 predictions.",
    )
    filter_lang_parser.add_argument(
        "--min-length", type=int, default=10, help="Minimum line length."
    )
    filter_lang_parser.add_argument("--k", type=int, default=2, help="Top-k languages.")
    filter_lang_parser.add_argument(
        "--model-path", help="Path to lid.176.bin (or set MULTILANG_PROBE_MODEL_PATH)."
    )

    extract_lang_parser = subparsers.add_parser(
        "extract-language", help="Extract passages for a single language."
    )
    extract_lang_parser.add_argument("--folder", required=True, help="Corpus folder path.")
    extract_lang_parser.add_argument(
        "--language", required=True, help="Target language code."
    )
    extract_lang_parser.add_argument(
        "--threshold", type=float, default=70, help="Confidence threshold (0-100)."
    )
    extract_lang_parser.add_argument(
        "--min-margin",
        type=float,
        default=0,
        help="Minimum probability margin between top-1 and top-2 predictions.",
    )
    extract_lang_parser.add_argument(
        "--min-length", type=int, default=10, help="Minimum line length."
    )
    extract_lang_parser.add_argument("--k", type=int, default=2, help="Top-k languages.")
    extract_lang_parser.add_argument(
        "--model-path", help="Path to lid.176.bin (or set MULTILANG_PROBE_MODEL_PATH)."
    )

    remove_parser = subparsers.add_parser(
        "remove-scripts", help="Remove characters from specific scripts or math symbols."
    )
    remove_parser.add_argument("--text", help="Text to analyze.")
    remove_parser.add_argument("--file", help="Path to a UTF-8 text file.")
    remove_parser.add_argument(
        "--scripts",
        help="Comma-separated list of script names to remove (e.g., cyrillic, greek).",
    )
    remove_parser.add_argument(
        "--remove-math",
        action="store_true",
        help="Remove mathematical symbols from the text.",
    )
    remove_parser.add_argument(
        "--remove-code",
        action="store_true",
        help="Remove code-like tokens from the text.",
    )

    extract_scripts_parser = subparsers.add_parser(
        "extract-scripts", help="Extract characters from specific scripts or math symbols."
    )
    extract_scripts_parser.add_argument("--text", help="Text to analyze.")
    extract_scripts_parser.add_argument("--file", help="Path to a UTF-8 text file.")
    extract_scripts_parser.add_argument(
        "--scripts",
        help="Comma-separated list of script names to extract (e.g., arabic, han).",
    )
    extract_scripts_parser.add_argument(
        "--include-math",
        action="store_true",
        help="Include mathematical symbols in the extracted output.",
    )
    extract_scripts_parser.add_argument(
        "--include-code",
        action="store_true",
        help="Include code-like tokens in the extracted output.",
    )
    extract_scripts_parser.add_argument(
        "--keep-whitespace",
        action="store_true",
        help="Keep whitespace in the extracted output.",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "classify-text":
        text = _load_text(args.text, args.file)
        _print_json(classify_text_with_proportions(text))
        return

    if args.command == "detect-language":
        text = _load_text(args.text, args.file)
        result = detect_language_fasttext(text, k=args.k, model_path=args.model_path)
        _print_json({"languages": result})
        return

    if args.command == "detect-math":
        text = _load_text(args.text, args.file)
        _print_json(detect_mathematical_language(text, threshold=args.threshold))
        return
    if args.command == "detect-code":
        text = _load_text(args.text, args.file)
        _print_json(detect_code_like_language(text, threshold=args.threshold))
        return

    if args.command == "visualize-scripts":
        text = _load_text(args.text, args.file)
        proportions = classify_text_with_proportions(text)
        output_path = plot_script_proportions(
            proportions, output_path=args.output, title=args.title or "Script proportions"
        )
        _print_json({"output": output_path, "proportions": proportions})
        return

    if args.command == "visualize-languages":
        results = analyze_corpus_with_fasttext(
            args.folder,
            k=args.k,
            model_path=args.model_path,
            min_length=args.min_length,
            block_size=args.block_size,
        )
        proportions_by_file = calculate_language_proportions(results)
        if args.file:
            proportions = proportions_by_file.get(args.file, {})
        else:
            proportions = _aggregate_language_proportions(results)
        output_path = plot_language_proportions(
            proportions, output_path=args.output, title=args.title or "Language proportions"
        )
        _print_json({"output": output_path, "proportions": proportions})
        return

    if args.command == "analyze-corpus":
        results = analyze_corpus_with_fasttext(
            args.folder,
            k=args.k,
            model_path=args.model_path,
            min_length=args.min_length,
            block_size=args.block_size,
        )
        _print_json(results)
        return

    if args.command == "language-proportions":
        results = analyze_corpus_with_fasttext(
            args.folder,
            k=args.k,
            model_path=args.model_path,
            min_length=args.min_length,
            block_size=args.block_size,
        )
        _print_json(calculate_language_proportions(results))
        return

    if args.command == "filter-by-characters":
        character_types = [item.strip() for item in args.types.split(",") if item.strip()]
        _print_json(
            filter_passages_by_character_types(
                args.folder, character_types, min_length=args.min_length
            )
        )
        return

    if args.command == "filter-by-language":
        languages = [item.strip() for item in args.languages.split(",") if item.strip()]
        results = analyze_corpus_with_fasttext(
            args.folder, k=args.k, model_path=args.model_path
        )
        _print_json(
            filter_passages_by_language(
                results,
                languages,
                args.folder,
                threshold=args.threshold,
                min_margin=args.min_margin,
                min_length=args.min_length,
                k=args.k,
                model_path=args.model_path,
            )
        )
        return

    if args.command == "extract-language":
        results = analyze_corpus_with_fasttext(
            args.folder, k=args.k, model_path=args.model_path
        )
        _print_json(
            extract_passages_improved(
                results,
                args.language,
                args.folder,
                threshold=args.threshold,
                min_margin=args.min_margin,
                min_length=args.min_length,
                k=args.k,
                model_path=args.model_path,
            )
        )
        return

    if args.command == "remove-scripts":
        text = _load_text(args.text, args.file)
        scripts = [item.strip() for item in args.scripts.split(",")] if args.scripts else []
        filtered_text = remove_scripts_and_math(
            text, scripts=scripts, remove_math=args.remove_math, remove_code=args.remove_code
        )
        _print_json({"text": filtered_text})
        return

    if args.command == "extract-scripts":
        text = _load_text(args.text, args.file)
        scripts = [item.strip() for item in args.scripts.split(",")] if args.scripts else []
        extracted_text = extract_scripts_and_math(
            text,
            scripts=scripts,
            include_math=args.include_math,
            include_code=args.include_code,
            keep_whitespace=args.keep_whitespace,
        )
        _print_json({"text": extracted_text})
        return


if __name__ == "__main__":
    main()
