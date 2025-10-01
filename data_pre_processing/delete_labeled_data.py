'''
4/4 prprocessing scripts 

Script to remove data from an ID in the files

removes the images in DATA_TO_DELETE from KIIT/full_data
'''
import os
import re
import json

JSON_INPUT = "KIIT/renamed_full_dataset.json"

JSON_OUTPUT = "KIIT/reorganized_full_dataset.json"

IMAGE_DIR = "KIIT/full_data"


DATA_TO_DELETE = [
        100,110,137,139,176,180,183,217,218,234,240,242,249,255,281,323,358,359,360,365,
        397,419,424,441,442,454,463,470,474,477,480,483,487,500,505,506,518,522,530,535,
        538,554,573,576,578,581,585,590,596,604,606,611,614,626,629,631,639,652,653,664,
        665,667,678,680,693,697,698,699,713,721,730,737,738,739,747,749,750,754,755,765,
        771,789,790,810,845,859,895,900,903,963,967,968,1003,1004,1007,1088,1099,1112,
        1119,1190,1215,1263,1204,1398,1316,1320,1326,1500,1407,1442,1469,1484,1593,1521,
        1541,1549,1560,1564,1594,1596,1622
]

def delete_data_by_image_id(data):
    images = data.get("images", [])
    annotations = data.get("annotations", [])

    # Remove images
    before_images = len(images)
    images[:] = [img for img in images if img["id"] not in DATA_TO_DELETE]
    removed_images = before_images - len(images)
    print(f"Removed {removed_images} images")

    # Remove annotations
    before_annotations = len(annotations)
    annotations[:] = [ann for ann in annotations if ann["image_id"] not in DATA_TO_DELETE]
    removed_annotations = before_annotations - len(annotations)
    print(f"Removed {removed_annotations} annotations")


def delete_kiit_images(directory, ids_to_delete):
    pattern = re.compile(r"^KIIT_(\d+)\.jpeg$", re.IGNORECASE)
    removed = 0
    ids_to_delete = set(ids_to_delete)  # faster lookup

    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            img_id = int(match.group(1))
            if img_id in ids_to_delete:
                file_path = os.path.join(directory, filename)
                try:
                    os.remove(file_path)
                    print(f"Deleted {file_path}")
                    removed += 1
                except Exception as e:
                    print(f"Could not delete {file_path}: {e}")

    print(f"\nDeleted {removed} files.")

if __name__ == "__main__":

    delete_kiit_images(IMAGE_DIR, DATA_TO_DELETE)

#    with open(JSON_INPUT, "r") as j:
#        data = json.load(j)
#
#    images = data.get("images", [])
#    annotations = data.get("annotations", [])
#
#    old_image_count = len(images)
#    old_annotation_count = len(annotations)
#
#    print(f"Original image count: {old_image_count}")
#    print(f"Original annotation count: {old_annotation_count}")
#
#    # Delete data
#    delete_data_by_image_id(data)
#
#    new_image_count = len(data["images"])
#    new_annotation_count = len(data["annotations"])
#
#    print(f"New image count: {new_image_count}")
#    print(f"New annotation count: {new_annotation_count}")
#    print(f"Removed {old_image_count - new_image_count} images")
#    print(f"Removed {old_annotation_count - new_annotation_count} annotations")
#
#    # Save new JSON
#    with open(JSON_OUTPUT, "w") as out:
#        json.dump(data, out, indent=2)
#
#    print(f"Cleaned dataset saved to {JSON_OUTPUT}")



