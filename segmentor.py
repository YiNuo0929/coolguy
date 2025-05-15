import cv2
import mediapipe as mp
import numpy as np

class Segmentor:
    def __init__(self, model_selection=1):
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.segmentor = self.mp_selfie_segmentation.SelfieSegmentation(model_selection=model_selection)

    def get_mask(self, frame):
        """
        輸入：BGR frame (來自 cv2.VideoCapture)
        輸出：segmentation mask（布林值陣列 True=人像, False=背景）
        """
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.segmentor.process(rgb)
        if result.segmentation_mask is not None:
            return result.segmentation_mask > 0.1  # 回傳布林 mask
        else:
            return np.zeros(frame.shape[:2], dtype=bool)