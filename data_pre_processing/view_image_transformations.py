import os
from PIL import Image
import matplotlib.pyplot as plt
import torchvision.transforms as T

def resize_and_pad_image(image, target_size=(448, 448)):
    """
    Resize image to fit within target_size while preserving aspect ratio, then pad to target_size.
    
    Args:
        image (PIL.Image): Input image.
        target_size (tuple): Desired output size (width, height).
    
    Returns:
        PIL.Image: Resized and padded image.
    """
    print(f"Resizing image to {target_size} while preserving aspect ratio")
    # Convert to RGB if needed
    if image.mode != 'RGB':
        print(f"Converting image mode from {image.mode} to RGB")
        image = image.convert('RGB')
    
    # Resize while maintaining aspect ratio
    original_size = image.size
    image.thumbnail(target_size, Image.Resampling.LANCZOS)
    print(f"Resized image from {original_size} to {image.size}")
    
    # Create a new blank image with target size and black background
    new_image = Image.new('RGB', target_size, (0, 0, 0))
    
    # Paste the resized image in the center
    offset = ((target_size[0] - image.size[0]) // 2,
              (target_size[1] - image.size[1]) // 2)
    print(f"Pasting image at offset {offset}")
    new_image.paste(image, offset)
    
    return new_image

def display_images(original, transformed, original_path, h, w):
    """
    Display original and transformed images side by side.
    
    Args:
        original (PIL.Image): Original image with specified resolution.
        transformed (PIL.Image): Transformed 448x448 image.
        original_path (str): Path to the original image.
        h (int): Original image height.
        w (int): Original image width.
    """
    print(f"Displaying images for {os.path.basename(original_path)}")
    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    
    # Display original image
    ax1.imshow(original)
    ax1.set_title(f"Original ({h}x{w}): {os.path.basename(original_path)}")
    ax1.axis('off')
    
    # Display transformed image
    ax2.imshow(transformed)
    ax2.set_title("Transformed (448x448)")
    ax2.axis('off')
    
    # Show plot and wait for keypress
    print("Press any key or click to continue to the next image...")
    plt.tight_layout()
    plt.show(block=False)
    plt.waitforbuttonpress()
    plt.close()
    print("Moving to next image\n")

def process_images_in_directory(directory, h, w):
    """
    Iterate through a directory, find images with specified resolution, and display them with their 448x448 versions.
    
    Args:
        directory (str): Path to the directory containing images.
        h (int): Target height for filtering images.
        w (int): Target width for filtering images.
    """
    print(f"Scanning directory: {directory}")
    # Ensure directory exists
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        return
    
    # Counter for processed images
    image_count = 0
    
    # Iterate through files in the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        
        try:
            # Open image
            with Image.open(file_path) as img:
                # Check if image matches specified resolution
                if img.size == (w, h):  # Note: img.size is (width, height)
                    image_count += 1
                    print(f"\nFound image #{image_count}: {filename} ({h}x{w})")
                    
                    # Load original image
                    original_img = img.copy()
                    
                    # Create 448x448 transformed version
                    print(f"Transforming {filename} to 448x448")
                    transformed_img = resize_and_pad_image(img, target_size=(448, 448))
                    
                    # Display both images
                    display_images(original_img, transformed_img, file_path, h, w)
                    
                else:
                    print(f"Skipping {filename}: Size {img.size}, expected ({w}, {h})")
                    
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            continue
    
    print(f"\nFinished processing. Total images with {h}x{w} resolution: {image_count}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python display_images.py <directory_path> <height> <width>")
        print("Example: python display_images.py /path/to/images 640 640")
        sys.exit(1)
    
    directory_path = sys.argv[1]
    try:
        h_old = int(sys.argv[2])
        w_old = int(sys.argv[3])
        print(f"Starting image processing for resolution {h_old}x{w_old}")
        process_images_in_directory(directory_path, h_old, w_old)
    except ValueError:
        print("Error: Height and width must be integers.")
        sys.exit(1)
