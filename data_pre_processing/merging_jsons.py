import json

JSON_INPUT_1 = "KIIT/reorganized_images1_800.json"
JSON_INPUT_2 = "KIIT/reorganized_images801_1623.json"
JSON_OUTPUT = "KIIT/full_KIIT_dataset.json"

def merge_coco(json1, json2):
    images1 = json1.get("images", [])
    images2 = json2.get("images", [])
    annotations1 = json1.get("annotations", [])
    annotations2 = json2.get("annotations", [])
    categories1 = json1.get("categories", [])
    categories2 = json2.get("categories", [])

    # Collect file_names to detect duplicates
    file_names = {img["file_name"] for img in images1}
    for img in images2:
        if img["file_name"] in file_names:
            raise ValueError(f"Duplicate image file name found: {img['file_name']}")
        file_names.add(img["file_name"])

    # Ensure unique image IDs
    max_img_id = max([img["id"] for img in images1], default=0)
    id_map = {}
    for img in images2:
        old_id = img["id"]
        max_img_id += 1
        img["id"] = max_img_id
        id_map[old_id] = img["id"]

    # Ensure unique annotation IDs
    max_ann_id = max([ann["id"] for ann in annotations1], default=0)
    for ann in annotations2:
        max_ann_id += 1
        ann["id"] = max_ann_id
        ann["image_id"] = id_map[ann["image_id"]]

    # Merge categories (assume same structure)
    if categories1 and categories2 and categories1 != categories2:
        raise ValueError("Category mismatch between datasets")

    merged = {
        "images": images1 + images2,
        "annotations": annotations1 + annotations2,
        "categories": categories1 or categories2
    }

    return merged

def main():
    with open(JSON_INPUT_1, "r") as f1, open(JSON_INPUT_2, "r") as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    merged = merge_coco(data1, data2)

    with open(JSON_OUTPUT, "w") as out:
        json.dump(merged, out, indent=2)

    print(f" Merged dataset saved to {JSON_OUTPUT}")
    print(f"  Total images: {len(merged['images'])}")
    print(f"  Total annotations: {len(merged['annotations'])}")

if __name__ == "__main__":
    main()

