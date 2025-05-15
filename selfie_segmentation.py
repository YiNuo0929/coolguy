import cv2
import mediapipe as mp
import numpy as np

# 初始化 mediapipe 的自拍分割模組
mp_selfie_segmentation = mp.solutions.selfie_segmentation

# 開啟 webcam
cap = cv2.VideoCapture(0)

# 自訂背景色（灰色），也可以改成圖片
BG_COLOR = (192, 192, 192)  # 背景顏色
bg_image = None  # 預設背景為空，稍後建立與畫面同大小的灰底圖

# 啟用 selfie segmentation 模型
with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as selfie_segmentation:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("忽略空畫面")
            continue

        # 水平翻轉畫面，轉成 RGB
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False  # 提升效能
        results = selfie_segmentation.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 建立 segmentation mask 的條件遮罩（人物位置）
        condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1

        # 建立背景圖（與攝影機畫面同尺寸）
        if bg_image is None:
            bg_image = np.zeros(image.shape, dtype=np.uint8)
            bg_image[:] = BG_COLOR

        # 合成：人像保留，背景替換
        output_image = np.where(condition, image, bg_image)

        # 顯示結果
        cv2.imshow('MediaPipe Selfie Segmentation', output_image)

        # 按下 ESC 鍵結束
        if cv2.waitKey(5) & 0xFF == 27:
            break

# 釋放資源
cap.release()
cv2.destroyAllWindows()