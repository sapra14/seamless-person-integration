import cv2
import numpy as np

def detect_shadows(bg_path, threshold=60):
    img = cv2.imread(bg_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Simple shadow detection by thresholding dark areas (tune threshold)
    _, shadow_mask = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY_INV)

    # Morphological ops to smooth shadow mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15,15))
    shadow_mask = cv2.morphologyEx(shadow_mask, cv2.MORPH_CLOSE, kernel)
    shadow_mask = cv2.GaussianBlur(shadow_mask, (21,21), 0)

    return shadow_mask
