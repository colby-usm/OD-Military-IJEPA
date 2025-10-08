import cv2
import json
import os

# Global variables for mouse callback
current_img = None
annotated_img = None
current_filename = ""

def show_coords(event, x, y, flags, param):
    """Mouse callback function to show coordinates and pixel color"""
    global current_img, annotated_img, current_filename
    
    if event == cv2.EVENT_MOUSEMOVE and annotated_img is not None:
        img_copy = annotated_img.copy()
        if 0 <= y < img_copy.shape[0] and 0 <= x < img_copy.shape[1]:
            # Display filename
            cv2.putText(img_copy, current_filename, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
            # Display coordinates
            cv2.putText(img_copy, f"X:{x}, Y:{y}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # Display pixel color
            b, g, r = img_copy[y, x]
            cv2.putText(img_copy, f"B:{b} G:{g} R:{r}", (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.imshow('COCO Dataset Viewer', img_copy)
            cv2.waitKey(1)  # Ensure the window refreshes

def load_coco_annotations(annotation_file):
    """Load COCO format annotations"""
    with open(annotation_file, 'r') as f:
        return json.load(f)

def get_category_name(category_id, categories):
    """Get category name from category ID"""
    for cat in categories:
        if cat['id'] == category_id:
            return cat['name']
    return 'Unknown'

def draw_annotations(img, annotations, categories):
    """Draw bounding boxes and labels on image"""
    for ann in annotations:
        x, y, w, h = map(int, ann['bbox'])
        category_name = get_category_name(ann['category_id'], categories)
        # Draw rectangle
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # Draw label background
        (label_w, label_h), baseline = cv2.getTextSize(category_name, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(img, (x, y - label_h - 5), (x + label_w, y), (0, 255, 0), -1)
        # Draw label text
        cv2.putText(img, category_name, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    return img

def main():
    global current_img, annotated_img, current_filename
    
    annotation_file = 'KIIT/annotations.json'
    image_dir = 'KIIT/images'
    
    # Load COCO annotations
    print("Loading COCO annotations...")
    coco_data = load_coco_annotations(annotation_file)
    images = coco_data['images']
    annotations = coco_data['annotations']
    categories = coco_data['categories']
    
    # Create mappings
    img_to_anns = {}
    filename_to_id = {}
    for img_info in images:
        img_id = img_info['id']
        filename = img_info['file_name']
        filename_to_id[filename] = img_id
    for ann in annotations:
        img_id = ann['image_id']
        if img_id not in img_to_anns:
            img_to_anns[img_id] = []
        img_to_anns[img_id].append(ann)
    
    print(f"Loaded {len(images)} images and {len(annotations)} annotations")
    print("Hover over image to see coordinates and pixel values")
    print("Enter an integer to select an image (KIIT_<num>.jpeg), or 'q' to quit.\n")
    
    # Create window and set mouse callback
    cv2.namedWindow('COCO Dataset Viewer')
    cv2.setMouseCallback('COCO Dataset Viewer', show_coords)
    
    while True:
        # Reset globals at start of loop to avoid old image caching
        current_img = None
        annotated_img = None
        current_filename = ""
        
        user_input = input("Enter image number (or 'q' to quit): ").strip()
        if user_input.lower() == 'q':
            print("Quitting...")
            break
        if not user_input.isdigit():
            print("Invalid input. Please enter an integer or 'q' to quit.")
            continue
        
        img_number = int(user_input)
        img_filename = f"KIIT_{img_number}.jpeg"
        img_path = os.path.join(image_dir, img_filename)
        
        if not os.path.exists(img_path):
            print(f"Image not found: {img_path}")
            continue
        
        # Load image
        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to load image: {img_path}")
            continue
        
        current_img = img.copy()
        current_filename = img_filename
        
        # Get annotations
        img_id = filename_to_id.get(img_filename)
        img_anns = img_to_anns.get(img_id, []) if img_id is not None else []
        
        # Draw annotations
        annotated_img = draw_annotations(img.copy(), img_anns, categories) if img_anns else img.copy()
        
        # Display image info
        print(f"{img_filename} - {len(img_anns)} annotations")
        cv2.imshow('COCO Dataset Viewer', annotated_img)
        
        # Wait for key press; break if 'q'
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q'):
            print("Quitting...")
            break

    # Clean up
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

