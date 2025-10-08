import json
from collections import Counter
import matplotlib.pyplot as plt

JSON_INPUT = "KIIT/labels.json"

def plot_class_distribution(json_file):
    # Load COCO dataset
    with open(json_file, "r") as f:
        data = json.load(f)

    annotations = data.get("annotations", [])
    categories = data.get("categories", [])

    # Map category_id -> category_name
    category_map = {cat["id"]: cat["name"] for cat in categories}

    # Count frequency of each category_id
    counts = Counter([ann["category_id"] for ann in annotations])

    # Prepare data for plotting
    labels = [category_map[cid] for cid in counts.keys()]
    values = [counts[cid] for cid in counts.keys()]

    # Plot bar chart
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, values)

    # Annotate bars with counts
    for bar, value in zip(bars, values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            str(value),
            ha="center",
            va="bottom",
            fontsize=9,
            fontweight="bold"
        )

    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Class")
    plt.ylabel("Number of Annotations")
    plt.title("Class Distribution in COCO Dataset")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_class_distribution(JSON_INPUT)

