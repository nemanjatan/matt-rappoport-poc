import cv2
import numpy as np
from PIL import Image
import os

def preprocess_image(image_path: str, output_path: str = None) -> Image.Image:
    """
    Load an image, apply preprocessing steps (grayscale, denoise, threshold, deskew),
    and return a PIL Image.
    
    Args:
        image_path: Path to the input image.
        output_path: Optional path to save the debug processed image.
        
    Returns:
        PIL.Image object of the processed image.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at {image_path}")

    # 1. Load image using OpenCV
    img = cv2.imread(image_path)
    if img is None:
         raise ValueError(f"Could not load image at {image_path}")

    # 2. Convert to Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. Denoise
    # h = parameter deciding filter strength. Higher h removes better noise but also removes details of image (10 is ok)
    denoised = cv2.fastNlMeansDenoising(gray, h=10)

    # 4. Thresholding (Binarization)
    # Binary thresholding often works well for clear scanned documents, 
    # but adaptive is better for varying lighting.
    # We'll use simple binary thresholding + Otsu's method as a robust baseline for black/white docs.
    _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 5. Deskewing
    # Find all coordinates of non-zero pixels (white text on black background)
    # Note: binary is white text on black background? 
    # Usually standard threshold gives black text on white background (if 255 is max).
    # Otsu results in: background (white) -> 255, text (black) -> 0.
    # To find text coordinates, we need to invert it so text is white (255).
    coords = np.column_stack(np.where(binary < 127)) # Text is dark
    
    angle = 0
    if len(coords) > 0:
        angle = cv2.minAreaRect(coords)[-1]
        
        # The cv2.minAreaRect() function returns values in the range [-90, 0).
        # as the rectangle rotates clockwise the returned angle trends to 0.
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
            
        # Re-rotate if angle is significant
        if abs(angle) > 0.5:
            (h, w) = binary.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            binary = cv2.warpAffine(binary, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # 6. Convert back to PIL Image
    pil_img = Image.fromarray(binary)
    
    if output_path:
        pil_img.save(output_path)
        
    return pil_img
