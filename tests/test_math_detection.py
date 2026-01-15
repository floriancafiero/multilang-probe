import unittest

from multilang_probe.math_detection import detect_mathematical_language


class TestMathDetection(unittest.TestCase):
    def test_detects_math_ratio(self):
        text = "x^2 + y^2 = r^2"
        result = detect_mathematical_language(text, threshold=1.0)
        self.assertGreater(result["math_symbols"], 0)
        self.assertGreater(result["total_characters"], 0)
        self.assertGreater(result["math_ratio"], 0.0)
        self.assertTrue(result["is_mathematical"])

    def test_empty_text(self):
        result = detect_mathematical_language("", threshold=1.0)
        self.assertEqual(result["math_symbols"], 0)
        self.assertEqual(result["total_characters"], 0)
        self.assertEqual(result["math_ratio"], 0.0)
        self.assertFalse(result["is_mathematical"])


if __name__ == "__main__":
    unittest.main()
