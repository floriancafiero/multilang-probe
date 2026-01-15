import tempfile
import unittest
from pathlib import Path

try:
    import matplotlib
except ModuleNotFoundError:  # pragma: no cover - handled in skip
    matplotlib = None

if matplotlib:
    matplotlib.use("Agg")
    from multilang_probe import visualization
else:
    visualization = None


@unittest.skipIf(visualization is None, "matplotlib is not available")
class TestVisualization(unittest.TestCase):
    def test_plot_script_proportions_saves(self):
        proportions = {"latin": 60.0, "cyrillic": 40.0}
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "scripts.png"
            result_path = visualization.plot_script_proportions(
                proportions, output_path=str(output_path)
            )
            self.assertEqual(result_path, str(output_path))
            self.assertTrue(output_path.exists())

    def test_plot_language_proportions_saves(self):
        proportions = {"fr": 70.0, "en": 30.0}
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "languages.png"
            result_path = visualization.plot_language_proportions(
                proportions, output_path=str(output_path)
            )
            self.assertEqual(result_path, str(output_path))
            self.assertTrue(output_path.exists())


if __name__ == "__main__":
    unittest.main()
