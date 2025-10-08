from PIL import Image
import sys

def resize_image(input_path, output_path, size=(224, 224)):
    """
    Resize an image to the specified size (default: 224x224) while maintaining aspect ratio.
    
    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the resized image.
        size (tuple): Desired output size (width, height).
    """
    try:
        img = Image.open(input_path)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize while maintaining aspect ratio
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        new_img = Image.new('RGB', size, (255, 255, 255))
        
        offset = ((size[0] - img.size[0]) // 2,
                 (size[1] - img.size[1]) // 2)
        new_img.paste(img, offset)
        
        new_img.save(output_path, 'JPEG')
        print(f"Image resized and saved to {output_path}")
        
    except Exception as e:
        print(f"Error processing image: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python resize_image.py <input_image_path> <output_image_path>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    resize_image(input_path, output_path)
