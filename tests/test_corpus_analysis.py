import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

sys.modules.setdefault("fasttext", types.SimpleNamespace(load_model=lambda _: None))

from multilang_probe import corpus_analysis


class TestCorpusAnalysis(unittest.TestCase):
    def test_analyze_corpus_with_blocks_and_min_length(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "sample.txt"
            file_path.write_text("Hi\nthere\n\nYo\n", encoding="utf-8")

            with mock.patch.object(
                corpus_analysis, "detect_language_fasttext", return_value="en: 99%"
            ) as mock_detect:
                results = corpus_analysis.analyze_corpus_with_fasttext(
                    tmpdir, k=1, min_length=3, block_size=2
                )

            mock_detect.assert_called_once_with("Hi there", k=1, model_path=None)
            self.assertEqual(results["sample.txt"], ["en: 99%"])

    def test_extract_passages_min_margin(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "sample.txt"
            file_path.write_text("Bonjour tout le monde\nSalut\n", encoding="utf-8")

            with mock.patch.object(
                corpus_analysis,
                "detect_language_fasttext_with_probs",
                side_effect=[
                    [("fr", 80.0), ("en", 70.0)],
                    [("fr", 90.0), ("en", 60.0)],
                ],
            ):
                results = corpus_analysis.extract_passages_improved(
                    {"sample.txt": []},
                    "fr",
                    tmpdir,
                    threshold=70,
                    min_margin=15,
                    min_length=1,
                    k=1,
                )

            self.assertEqual(results["sample.txt"], [(2, "Salut")])

    def test_filter_passages_min_margin_respects_top_language(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "sample.txt"
            file_path.write_text("Hello world\nBonjour\n", encoding="utf-8")

            with mock.patch.object(
                corpus_analysis,
                "detect_language_fasttext_with_probs",
                side_effect=[
                    [("en", 90.0), ("fr", 80.0)],
                    [("fr", 85.0), ("en", 70.0)],
                ],
            ):
                results = corpus_analysis.filter_passages_by_language(
                    {"sample.txt": []},
                    ["fr"],
                    tmpdir,
                    threshold=70,
                    min_margin=10,
                    min_length=1,
                    k=1,
                )

            self.assertEqual(results["sample.txt"], [(2, "Bonjour")])


if __name__ == "__main__":
    unittest.main()
