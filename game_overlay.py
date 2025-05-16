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

def overlay_on_background(bg, fg, position):
    """
    將含透明背景的前景圖 fg 貼到背景圖 bg 上，position 為 (x, y)
    x, y 是貼圖的左上角位置
    """
    x, y = position
    fg_h, fg_w = fg.shape[:2]
    bg_h, bg_w = bg.shape[:2]

    # 防止超出邊界
    if x < 0: x = 0
    if y < 0: y = 0
    if x + fg_w > bg_w:
        fg = fg[:, :bg_w - x]
    if y + fg_h > bg_h:
        fg = fg[:bg_h - y, :]

    fg_h, fg_w = fg.shape[:2]
    roi = bg[y:y + fg_h, x:x + fg_w]

    fg_rgb = fg[:, :, :3]
    fg_alpha = fg[:, :, 3:] / 255.0
    bg_part = roi * (1 - fg_alpha)
    fg_part = fg_rgb * fg_alpha
    bg[y:y + fg_h, x:x + fg_w] = (bg_part + fg_part).astype(np.uint8)

    return bg