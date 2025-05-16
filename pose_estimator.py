import mediapipe as mp
import cv2
import math

class PoseEstimator:
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def calculate_angle(self, a, b, c):
        a = [a.x, a.y]
        b = [b.x, b.y]
        c = [c.x, c.y]

        radians = math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0])
        angle = abs(radians*180.0/math.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle

    def detect_pose(self, frame):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)

        if not results.pose_landmarks:
            return 'neutral'

        lm = results.pose_landmarks.landmark

        l_shoulder = lm[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
        r_shoulder = lm[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
        l_hip = lm[self.mp_pose.PoseLandmark.LEFT_HIP]
        r_hip = lm[self.mp_pose.PoseLandmark.RIGHT_HIP]
        l_ankle = lm[self.mp_pose.PoseLandmark.LEFT_ANKLE]
        r_ankle = lm[self.mp_pose.PoseLandmark.RIGHT_ANKLE]
        l_wrist = lm[self.mp_pose.PoseLandmark.LEFT_WRIST]
        r_wrist = lm[self.mp_pose.PoseLandmark.RIGHT_WRIST]
        '''
        # 原本的 hi 檢查（只要任一手高於肩膀）
        if l_wrist.y < l_shoulder.y or r_wrist.y < r_shoulder.y:
            return 'hi'
        '''
        # 簡單左右跳躍控制
        right_up = l_wrist.y < l_shoulder.y
        left_up = r_wrist.y < r_shoulder.y

        if left_up and right_up:
            return 'jump'
        elif left_up:
            return 'left'
        elif right_up:
            return 'right'

        return 'neutral'
'''
import mediapipe as mp
import cv2
import math

class PoseEstimator:
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def calculate_angle(self, a, b, c):
        """計算三個點之間的角度"""
        a = [a.x, a.y]
        b = [b.x, b.y]
        c = [c.x, c.y]

        radians = math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0])
        angle = abs(radians*180.0/math.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle

    def detect_pose(self, frame):
        """
        輸入：BGR 影像，輸出：姿勢標籤之一 ['left', 'right', 'jump', 'hi', 'neutral']
        """
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)

        if not results.pose_landmarks:
            return 'neutral'  # 無偵測到人

        lm = results.pose_landmarks.landmark

        # 簡化名稱
        l_shoulder = lm[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
        r_shoulder = lm[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
        l_hip = lm[self.mp_pose.PoseLandmark.LEFT_HIP]
        r_hip = lm[self.mp_pose.PoseLandmark.RIGHT_HIP]
        l_ankle = lm[self.mp_pose.PoseLandmark.LEFT_ANKLE]
        r_ankle = lm[self.mp_pose.PoseLandmark.RIGHT_ANKLE]
        l_wrist = lm[self.mp_pose.PoseLandmark.LEFT_WRIST]
        r_wrist = lm[self.mp_pose.PoseLandmark.RIGHT_WRIST]

        # 計算肩膀與臀部的連線角度
        shoulder_hip_angle = self.calculate_angle(l_shoulder, l_hip, r_hip)

        # 判斷跳躍（腳踝高於臀部）
        avg_hip_y = (l_hip.y + r_hip.y) / 2
        avg_ankle_y = (l_ankle.y + r_ankle.y) / 2
        if avg_ankle_y < avg_hip_y - 0.1:
            return 'jump'

        # 判斷揮手（手腕高於肩膀）
        if l_wrist.y < l_shoulder.y or r_wrist.y < r_shoulder.y:
            return 'hi'

        # 判斷左右移動
        if shoulder_hip_angle > 10 and shoulder_hip_angle < 45:
            return 'right'
        elif shoulder_hip_angle > 135 and shoulder_hip_angle < 170:
            return 'left'

        return 'neutral'
'''