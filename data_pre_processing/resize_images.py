import os
import cv2
from PIL import Image
import json

# Constants
MIN_SIZE = 480
MAX_SIZE_SHORT = 800
MAX_SIZE_LONG = 1333

IMAGES_DIR = "KIIT/image_data"
OUTPUT_DIR = "KIIT/resized_image_data"
ANNOTATIONS_FILE = "KIIT/labels.json"
OUTPUT_ANNOTATIONS_FILE = "KIIT/resized_labels.json"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(ANNOTATIONS_FILE, "r") as f:
    coco = json.load(f)

image_id_map = {}  # old image_id -> new info
new_image_id = 1
new_ann_id = 1
images_to_drop = []
new_images = []
new_annotations = []

for img in coco["images"]:
    img_path = os.path.join(IMAGES_DIR, img["file_name"])
    if not os.path.exists(img_path):
        print(f"Warning: Image not found: {img_path}")
        images_to_drop.append(img["file_name"])
        continue

    # Read image with OpenCV
    im = cv2.imread(img_path)
    if im is None:
        print(f"Warning: Could not read image: {img_path}")
        images_to_drop.append(img["file_name"])
        continue

    h, w = im.shape[:2]
    min_side = min(w, h)
    max_side = max(w, h)

    # Check if image is within acceptable range
    if not (MIN_SIZE <= min_side <= MAX_SIZE_SHORT and max_side <= MAX_SIZE_LONG):
        images_to_drop.append(img["file_name"])
        continue

    # Convert to PIL for resizing
    im = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))

    # Calculate scale factor
    scale = 1.0
    if min_side < MAX_SIZE_SHORT:
        scale = MAX_SIZE_SHORT / min_side
    if max_side * scale > MAX_SIZE_LONG:
        scale = MAX_SIZE_LONG / max_side

    new_w = int(round(w * scale))
    new_h = int(round(h * scale))

    # Resize image
    im_resized = im.resize((new_w, new_h), Image.BILINEAR)
    out_path = os.path.join(OUTPUT_DIR, img["file_name"])
    im_resized.save(out_path)

    # Save mapping for bbox scaling
    image_id_map[img["id"]] = {
        "new_id": new_image_id,
        "scale_x": new_w / w,
        "scale_y": new_h / h
    }

    # Save resized image info
    new_img = img.copy()
    new_img["width"] = new_w
    new_img["height"] = new_h
    new_img["id"] = new_image_id
    new_images.append(new_img)
    new_image_id += 1

print(f"\nKept {len(new_images)} out of {len(coco['images'])} images")
if images_to_drop:
    print(f"\nImages to drop ({len(images_to_drop)}):")
    print("<" + ", ".join(images_to_drop) + ">")
else:
    print("\n✓ All images are within acceptable size range")

# Resize annotations
for ann in coco["annotations"]:
    old_img_id = ann["image_id"]
    if old_img_id not in image_id_map:
        continue  # image was dropped

    new_ann = ann.copy()
    img_info = image_id_map[old_img_id]
    scale_x = img_info["scale_x"]
    scale_y = img_info["scale_y"]

    # Scale bbox
    x, y, bw, bh = ann["bbox"]
    new_ann["bbox"] = [x * scale_x, y * scale_y, bw * scale_x, bh * scale_y]

    # Scale segmentation if present
    if "segmentation" in ann and ann["segmentation"]:
        new_seg = []
        for seg in ann["segmentation"]:
            if isinstance(seg, list):
                scaled_seg = []
                for i in range(0, len(seg), 2):
                    scaled_seg.append(seg[i] * scale_x)
                    scaled_seg.append(seg[i+1] * scale_y)
                new_seg.append(scaled_seg)
            else:
                new_seg.append(seg)  # RLE
        new_ann["segmentation"] = new_seg

    # Scale area
    if "area" in ann:
        new_ann["area"] = ann["area"] * scale_x * scale_y

    new_ann["image_id"] = img_info["new_id"]
    new_ann["id"] = new_ann_id
    new_annotations.append(new_ann)
    new_ann_id += 1

print(f"Kept {len(new_annotations)} out of {len(coco['annotations'])} annotations")

# Save new annotations
new_coco = {
    "images": new_images,
    "annotations": new_annotations,
    "categories": coco.get("categories", [])
}
# Preserve other fields
for key in coco:
    if key not in ["images", "annotations", "categories"]:
        new_coco[key] = coco[key]

with open(OUTPUT_ANNOTATIONS_FILE, "w") as f:
    json.dump(new_coco, f, indent=2)

print(f"\nSaved resized images to: {OUTPUT_DIR}")
print(f"Saved updated annotations to: {OUTPUT_ANNOTATIONS_FILE}")

