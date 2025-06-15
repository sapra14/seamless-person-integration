import cv2
import numpy as np

def generate_shadow(fg_path, bg_shape, light_dir, output_path, intensity=0.6, blur_size=25):
    fg = cv2.imread(fg_path, cv2.IMREAD_UNCHANGED)
    alpha = fg[:, :, 3] / 255.0 if fg.shape[2] == 4 else np.ones(fg.shape[:2])

    # Create shadow mask (black silhouette)
    shadow_mask = (alpha * 255).astype(np.uint8)

    # Create black image for shadow
    shadow = np.zeros((bg_shape[0], bg_shape[1]), dtype=np.uint8)

    # Position shadow offset based on light_dir
    offset_x = int(light_dir[0] * 50)  # Distance can be adjusted
    offset_y = int(light_dir[1] * 50)

    # Place shadow mask shifted by offset on black bg
    shadow[max(0, offset_y):max(0, offset_y)+shadow_mask.shape[0],
           max(0, offset_x):max(0, offset_x)+shadow_mask.shape[1]] = shadow_mask

    # Blur to soften shadow edges
    shadow = cv2.GaussianBlur(shadow, (blur_size, blur_size), 0)

    # Save shadow image (you can also blend this with background)
    cv2.imwrite(output_path, shadow)
