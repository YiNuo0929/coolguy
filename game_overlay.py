import cv2
import numpy as np

def extract_foreground(image, mask):
    fg = np.zeros_like(image, dtype=np.uint8)
    fg[mask] = image[mask]

    alpha = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    alpha[mask] = 255

    rgba = cv2.merge((fg, alpha))  # B, G, R, A
    return rgba

def resize_foreground(fg_rgba, scale=0.3):
    h, w = fg_rgba.shape[:2]
    new_size = (int(w * scale), int(h * scale))
    return cv2.resize(fg_rgba, new_size, interpolation=cv2.INTER_AREA)

def overlay_on_background(background, fg_rgba, position='center'):
    bg_h, bg_w = background.shape[:2]
    fg_h, fg_w = fg_rgba.shape[:2]

    if isinstance(position, str):
        if position == 'center':
            x = (bg_w - fg_w) // 2
            y = (bg_h - fg_h) // 2
        elif position == 'bottom_center':
            x = (bg_w - fg_w) // 2
            y = bg_h - fg_h - 30
        else:
            x, y = 0, 0
    else:
        x, y = position

    # 限制範圍，避免出界
    if x + fg_w > bg_w or y + fg_h > bg_h:
        return background

    roi = background[y:y+fg_h, x:x+fg_w]
    b, g, r, a = cv2.split(fg_rgba)
    alpha = a.astype(float) / 255.0
    alpha_inv = 1.0 - alpha

    for c in range(3):
        roi[:, :, c] = (alpha * fg_rgba[:, :, c] + alpha_inv * roi[:, :, c]).astype(np.uint8)

    background[y:y+fg_h, x:x+fg_w] = roi
    return background