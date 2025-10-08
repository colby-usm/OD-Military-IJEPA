import cv2
import json
import os
from pathlib import Path

# Global variables for mouse callback
current_img = None
annotated_img = None
current_filename = ""

def show_coords(event, x, y, flags, param):
    """Mouse callback function to show coordinates and pixel color"""
    global current_img, annotated_img, current_filename
    
    if event == cv2.EVENT_MOUSEMOVE and annotated_img is not None:
        # Create a copy to draw on
        img_copy = annotated_img.copy()
        
        # Ensure coordinates are within image bounds
        if 0 <= y < img_copy.shape[0] and 0 <= x < img_copy.shape[1]:
            # Display image filename
            cv2.putText(img_copy, current_filename, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
            
            # Display coordinates
            text = f"X: {x}, Y: {y}"
            cv2.putText(img_copy, text, (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Show pixel color
            b, g, r = img_copy[y, x]
            color_text = f"B:{b} G:{g} R:{r}"
            cv2.putText(img_copy, color_text, (10, 110),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('COCO Dataset Viewer', img_copy)

def load_coco_annotations(annotation_file):
    """Load COCO format annotations"""
    with open(annotation_file, 'r') as f:
        coco_data = json.load(f)
    return coco_data

def get_category_name(category_id, categories):
    """Get category name from category ID"""
    for cat in categories:
        if cat['id'] == category_id:
            return cat['name']
    return 'Unknown'

def draw_annotations(img, annotations, categories):
    """Draw bounding boxes and labels on image"""
    for ann in annotations:
        # Get bounding box coordinates (COCO format: [x, y, width, height])
        x, y, w, h = map(int, ann['bbox'])
        
        # Get category name
        category_name = get_category_name(ann['category_id'], categories)
        
        # Draw rectangle
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Draw label background
        label = f"{category_name}"
        (label_w, label_h), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(img, (x, y - label_h - 5), (x + label_w, y), (0, 255, 0), -1)
        
        # Draw label text
        cv2.putText(img, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    return img

def main():
    global current_img, annotated_img, current_filename
    
    # Configuration
    annotation_file = 'annotations.json'
    image_dir = 'images'
    
    # Load COCO annotations
    print("Loading COCO annotations...")
    coco_data = load_coco_annotations(annotation_file)
    
    images = coco_data['images']
    annotations = coco_data['annotations']
    categories = coco_data['categories']
    
    # Create a mapping of image_id to annotations
    img_to_anns = {}
    for ann in annotations:
        img_id = ann['image_id']
        if img_id not in img_to_anns:
            img_to_anns[img_id] = []
        img_to_anns[img_id].append(ann)
    
    print(f"Loaded {len(images)} images and {len(annotations)} annotations")
    print("Hover over image to see coordinates and pixel values")
    print("Press any key to view next image, 'q' to quit\n")
    
    # Create window and set mouse callback
    cv2.namedWindow('COCO Dataset Viewer')
    cv2.setMouseCallback('COCO Dataset Viewer', show_coords)
    
    # Iterate through images
    for idx, img_info in enumerate(images):
        img_id = img_info['id']
        img_filename = img_info['file_name']
        img_path = os.path.join(image_dir, img_filename)
        
        # Check if image exists
        if not os.path.exists(img_path):
            print(f"Image not found: {img_path}")
            continue
        
        # Load image
        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to load image: {img_path}")
            continue
        
        # Store current image and filename
        current_img = img.copy()
        current_filename = img_filename
        
        # Get annotations for this image
        img_anns = img_to_anns.get(img_id, [])
        
        # Draw annotations
        if img_anns:
            annotated_img = draw_annotations(img.copy(), img_anns, categories)
        else:
            annotated_img = img.copy()
        
        # Display image info
        print(f"[{idx + 1}/{len(images)}] {img_filename} - {len(img_anns)} annotations")
        
        # Show image
        cv2.imshow('COCO Dataset Viewer', annotated_img)
        
        # Wait for key press
        key = cv2.waitKey(0) & 0xFF
        
        # Check if 'q' was pressed
        if key == ord('q'):
            print("Quitting...")
            break
    
    # Clean up
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
