import os
import json

# Paths
IMAGES_DIR = "images"
ANNOTATIONS_FILE = "annotations.json"

# Load COCO annotations
with open(ANNOTATIONS_FILE, "r") as f:
    coco = json.load(f)

missing_images = []

for img in coco["images"]:
    img_path = os.path.join(IMAGES_DIR, img["file_name"])
    if not os.path.exists(img_path):
        missing_images.append(img["file_name"])

if missing_images:
    print(f"Missing {len(missing_images)} images:")
    for fname in missing_images:
        print(" -", fname)
else:
    print("All images are present in the directory.")
