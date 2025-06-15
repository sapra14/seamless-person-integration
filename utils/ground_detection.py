# utils/ground_detection.py
import cv2
import numpy as np

def detect_ground_line_y(bg_path, debug=False):
    bg = cv2.imread(bg_path)
    gray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)

    # Edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Hough lines detection
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

    if lines is None:
        return int(bg.shape[0] * 0.9)

    ground_y = None
    max_length = 0
    height = bg.shape[0]

    for line in lines:
        x1, y1, x2, y2 = line[0]
        length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
        if abs(angle) < 10 or abs(angle) > 170:
            if y1 > height * 0.75 and y2 > height * 0.75:
                if length > max_length:
                    max_length = length
                    ground_y = int((y1 + y2) / 2)

    if ground_y is None:
        ground_y = int(height * 0.9)

    if debug:
        import matplotlib.pyplot as plt
        bg_copy = bg.copy()
        for line in lines:
            x1, y1, x2, y2 = line[0]
            color = (0, 255, 0) if int((y1 + y2) / 2) == ground_y else (0, 0, 255)
            cv2.line(bg_copy, (x1, y1), (x2, y2), color, 2)
        cv2.line(bg_copy, (0, ground_y), (bg.shape[1], ground_y), (255,0,0), 3)
        plt.imshow(cv2.cvtColor(bg_copy, cv2.COLOR_BGR2RGB))
        plt.title('Detected Ground Line')
        plt.show()

    return ground_y
