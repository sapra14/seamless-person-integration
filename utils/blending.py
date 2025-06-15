import cv2
import numpy as np
from utils.ground_detection import detect_ground_line_y

def blend_images_auto_position(fg_path, bg_path, output_path, scale_ratio=0.6, debug=False):
    bg = cv2.imread(bg_path)
    fg = cv2.imread(fg_path, cv2.IMREAD_UNCHANGED)

    if fg is None or bg is None:
        raise ValueError("Foreground or background image not found or cannot be read.")

    if fg.shape[2] != 4:
        raise ValueError("Foreground image must have alpha channel (RGBA).")

    fg_rgb = fg[:, :, :3]
    alpha = fg[:, :, 3] / 255.0

    # Resize foreground
    new_width = int(bg.shape[1] * scale_ratio)
    scale = new_width / fg.shape[1]
    fg_rgb = cv2.resize(fg_rgb, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    alpha = cv2.resize(alpha, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

    h_fg, w_fg = fg_rgb.shape[:2]

    # Detect ground line y on background image
    ground_y = detect_ground_line_y(bg_path, debug=debug)

    # Position so that fg feet align with ground line
    x = (bg.shape[1] - w_fg) // 2
    y = ground_y - h_fg
    y = max(0, y)  # clamp to top if negative

    if debug:
        print(f"Background shape: {bg.shape}")
        print(f"Foreground resized to: {w_fg}x{h_fg}")
        print(f"Ground line y: {ground_y}")
        print(f"Blending position (x, y): ({x}, {y})")

    # Blend using alpha mask
    roi = bg[y:y+h_fg, x:x+w_fg].astype(np.float32)
    for c in range(3):
        roi[:, :, c] = alpha * fg_rgb[:, :, c] + (1 - alpha) * roi[:, :, c]

    bg[y:y+h_fg, x:x+w_fg] = roi.astype(np.uint8)

    cv2.imwrite(output_path, bg)
