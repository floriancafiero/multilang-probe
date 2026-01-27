import unittest

from multilang_probe.text_filtering import extract_scripts_and_math, remove_scripts_and_math


class TestTextFiltering(unittest.TestCase):
    def test_remove_scripts(self):
        text = "Hello Привет 123"
        filtered = remove_scripts_and_math(text, scripts=["cyrillic"], remove_math=False)
        self.assertEqual(filtered, "Hello  123")

    def test_remove_math(self):
        text = "x^2 + y^2 = 5"
        filtered = remove_scripts_and_math(text, scripts=[], remove_math=True)
        self.assertNotIn("+", filtered)
        self.assertNotIn("=", filtered)
        self.assertNotIn("^", filtered)

    def test_extract_scripts_and_math(self):
        text = "Hi Привет +="
        extracted = extract_scripts_and_math(
            text, scripts=["cyrillic"], include_math=True, keep_whitespace=False
        )
        self.assertEqual(extracted, "Привет+=")

    def test_extract_scripts_keep_whitespace(self):
        text = "Hi Привет +="
        extracted = extract_scripts_and_math(
            text, scripts=["cyrillic"], include_math=True, keep_whitespace=True
        )
        self.assertEqual(extracted, " Привет +=")


if __name__ == "__main__":
    unittest.main()
