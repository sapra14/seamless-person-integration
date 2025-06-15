# utils/lighting_estimation.py
import cv2
import numpy as np

def detect_shadows(image):
    """
    Detect shadows in the background image.
    Returns a binary mask of shadow regions.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Threshold to detect dark regions (shadows)
    _, shadow_mask = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    return shadow_mask

def estimate_light_direction(shadow_mask):
    """
    Estimate the light direction from shadow mask.
    Returns a 2D unit vector indicating light direction.
    """
    contours, _ = cv2.findContours(shadow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return np.array([0, 1])  # Default downward light if no shadows detected
    
    largest_contour = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(largest_contour)
    angle = rect[-1]
    
    # Convert angle to radians and create direction vector
    rad = np.deg2rad(angle)
    light_dir = np.array([np.cos(rad), np.sin(rad)])
    return light_dir
