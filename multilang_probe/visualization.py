from pathlib import Path

import matplotlib.pyplot as plt


def _save_or_show(fig, output_path):
    if output_path:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output, bbox_inches="tight")
        return str(output)
    fig.show()
    return None


def plot_script_proportions(proportions, output_path=None, title="Script proportions"):
    labels = list(proportions.keys())
    values = list(proportions.values())
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, values, color="#4C78A8")
    ax.set_ylabel("Percentage")
    ax.set_title(title)
    ax.set_ylim(0, max(values) * 1.2 if values else 1)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return _save_or_show(fig, output_path)


def plot_language_proportions(
    proportions, output_path=None, title="Language proportions"
):
    labels = list(proportions.keys())
    values = list(proportions.values())
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, values, color="#F58518")
    ax.set_ylabel("Percentage")
    ax.set_title(title)
    ax.set_ylim(0, max(values) * 1.2 if values else 1)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return _save_or_show(fig, output_path)
