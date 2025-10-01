#!/usr/bin/env python3
"""
Normalize COCO JSON for KIIT dataset:
- Renames 'images[*].file_name' -> KIIT_<seq>.jpeg
- Reassigns 'images[*].id' to a new sequential ID
- Updates 'annotations[*].image_id' to match new IDs
"""
import json
import re

JSON_INPUT = "KIIT/full_KIIT_dataset.json"
JSON_OUTPUT = "KIIT/renamed_full_dataset.json"

def main():
    with open(JSON_INPUT, "r") as j:
        data = json.load(j)

    images = data.get("images", [])
    annotations = data.get("annotations", [])

    # Map old_id -> new_id
    id_map = {}

    for img in images:
        old_id = img["id"]
        file_name = img["file_name"]

        # Extract KIIT_xxx number from the filename
        match = re.search(r"KIIT_(\d+)", file_name)
        if not match:
            raise ValueError(f"Could not extract KIIT number from {file_name}")

        number = int(match.group(1))
        new_filename = f"KIIT_{number}.jpeg"

        # Update image fields
        img["file_name"] = new_filename
        img["id"] = number

        id_map[old_id] = number

        print(f"Image: old id {old_id} -> new id {number}, {file_name} -> {new_filename}")

    # Update annotations
    updated = 0
    for ann in annotations:
        old_img_id = ann["image_id"]
        if old_img_id in id_map:
            ann["image_id"] = id_map[old_img_id]
            updated += 1

    with open(JSON_OUTPUT, "w") as out:
        json.dump(data, out, indent=2)

    print("\nFinished processing")
    print(f"  Images updated: {len(images)}")
    print(f"  Annotations updated: {updated}")
    print(f"  Saved to: {JSON_OUTPUT}")


if __name__ == "__main__":
    main()

