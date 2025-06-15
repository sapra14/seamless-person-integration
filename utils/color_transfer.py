import cv2
import numpy as np

def reinhard_color_transfer(source_path, target_path, output_path, blend_factor=0.3):
    """
    Applies Reinhard color transfer to harmonize color between source and target,
    but limits the effect with blend_factor to avoid faded appearance.
    """
    source = cv2.imread(source_path, cv2.IMREAD_UNCHANGED)
    target = cv2.imread(target_path)

    if source.shape[2] != 4:
        raise ValueError("Source image must have an alpha channel (RGBA).")

    source_rgb = source[:, :, :3].astype(np.float32)
    alpha = source[:, :, 3] / 255.0
    mask = alpha > 0

    # Compute stats from masked person and entire target image
    masked_pixels = source_rgb[mask]
    target_pixels = target.reshape((-1, 3)).astype(np.float32)

    src_mean = np.mean(masked_pixels, axis=0)
    src_std = np.std(masked_pixels, axis=0)
    tgt_mean = np.mean(target_pixels, axis=0)
    tgt_std = np.std(target_pixels, axis=0)

    src_std = np.where(src_std == 0, 1.0, src_std)

    # Apply color transfer with blend_factor
    result = source_rgb.copy()
    for c in range(3):
        original = result[:, :, c]
        transfer = ((original - src_mean[c]) * (tgt_std[c] / src_std[c]) + tgt_mean[c])
        result[:, :, c] = np.where(mask, 
                                   (1 - blend_factor) * original + blend_factor * transfer, 
                                   original)

    result = np.clip(result, 0, 255).astype(np.uint8)

    output = cv2.merge([
        result[:, :, 0],
        result[:, :, 1],
        result[:, :, 2],
        (alpha * 255).astype(np.uint8)
    ])

    cv2.imwrite(output_path, output)
