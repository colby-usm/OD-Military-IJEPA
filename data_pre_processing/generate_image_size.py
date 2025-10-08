#!/usr/bin/env python3
"""
plot_image_sizes_categorical.py
Plots a pie chart showing the distribution of the top k image sizes in a directory
with categorical labels and prints image size, count, and total percentage.
"""

import os
import sys
from collections import Counter
from PIL import Image
import matplotlib.pyplot as plt

def get_image_sizes(image_dir):
    sizes = []
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')
    for filename in os.listdir(image_dir):
        if filename.lower().endswith(supported_formats):
            path = os.path.join(image_dir, filename)
            try:
                with Image.open(path) as img:
                    sizes.append(img.size)  # (width, height)
            except Exception as e:
                print(f"Warning: could not open {filename}: {e}")
    return sizes

def plot_size_distribution(sizes, k):
    size_counts = Counter(sizes)
    # Sort by count (descending) and then by resolution (ascending) for tie-breaking
    sorted_sizes = sorted(size_counts.items(), key=lambda x: (-x[1], x[0][0], x[0][1]))
    # Take top k resolutions
    top_k_sizes = sorted_sizes[:k]
    labels = [f"{w}x{h}" for (w, h), _ in top_k_sizes]
    counts = [count for _, count in top_k_sizes]
    
    if not labels:
        print("No image sizes available to plot.")
        return
    
    # Calculate total images and print results
    total_images = sum(counts)
    print("Image Size, Count, Total Percentage")
    for label, count in zip(labels, counts):
        percentage = (count / total_images * 100) if total_images > 0 else 0
        print(f"{label}, {count}, {percentage:.1f}%")
    
    # Generate pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=labels, autopct='%1.1f%%', colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD'])
    plt.title(f"Top {k} Image Size Distribution")
    plt.tight_layout()
    plt.show()

def main():
    if len(sys.argv) != 3:
        print("Usage: python plot_image_sizes_categorical.py /path/to/images k")
        sys.exit(1)
    
    image_dir = sys.argv[1]
    try:
        k = int(sys.argv[2])
        if k <= 0:
            print("Error: k must be a positive integer.")
            sys.exit(1)
    except ValueError:
        print("Error: k must be an integer.")
        sys.exit(1)
    
    sizes = get_image_sizes(image_dir)
    
    if not sizes:
        print("No images found in the directory.")
        sys.exit(1)
    
    # Ensure k does not exceed the number of unique sizes
    unique_sizes = len(set(sizes))
    if k > unique_sizes:
        print(f"Warning: k={k} exceeds number of unique sizes ({unique_sizes}). Using k={unique_sizes}.")
        k = unique_sizes
    
    plot_size_distribution(sizes, k)

if __name__ == "__main__":
    main()
