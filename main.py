import cv2
import numpy as np
import time
from segmentor import Segmentor
from game_overlay import extract_foreground, resize_foreground, overlay_on_background
from pose_estimator import PoseEstimator
from character_controller import CharacterController

# 初始化
cap = cv2.VideoCapture(0)
segmentor = Segmentor()
pose_estimator = PoseEstimator()

# 先抓一張 frame 來取得攝影機畫面大小
ret, frame = cap.read()
if not ret:
    raise RuntimeError("無法從攝影機取得影像")
frame = cv2.flip(frame, 1)
h, w = frame.shape[:2]

# 背景圖調整為與攝影機畫面一樣大
bg_image = cv2.imread("bg.jpg")
if bg_image is None:
    bg_image = np.zeros((h, w, 3), dtype=np.uint8)
    bg_image[:] = (100, 200, 255)
else:
    bg_image = cv2.resize(bg_image, (w, h))

# 控制器初始化
controller = CharacterController(canvas_width=w, canvas_height=h, scale=0.3)
character_initialized = False

# 遊戲主迴圈
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # 偵測動作
    action = pose_estimator.detect_pose(frame)

    # 分割人物
    mask = segmentor.get_mask(frame)
    fg_rgba = extract_foreground(frame, mask)
    fg_small = resize_foreground(fg_rgba, scale=controller.scale)

    # 初始化角色位置
    if not character_initialized:
        fg_h, fg_w = fg_small.shape[:2]
        gray_mask = cv2.cvtColor(fg_rgba, cv2.COLOR_BGRA2GRAY)
        x_indices = np.where(gray_mask > 10)[1]
        if len(x_indices) > 0:
            initial_center_x = int(np.mean(x_indices))
        else:
            initial_center_x = w // 2

        controller.set_character_size(fg_w, fg_h, initial_center_x=initial_center_x)
        character_initialized = True

    # 更新畫面
    canvas = bg_image.copy()
    if character_initialized:
        controller.update(action)
        pos = controller.get_position()
        canvas = overlay_on_background(canvas, fg_small, position=pos)
        cv2.putText(canvas, f"Pose: {action}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
    else:
        cv2.putText(canvas, "請站到畫面中", (80, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 100, 200), 2)

    cv2.imshow("Game Pose Control", canvas)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
'''
import cv2
import numpy as np
import time
from segmentor import Segmentor
from game_overlay import extract_foreground, resize_foreground, overlay_on_background
from pose_estimator import PoseEstimator
from character_controller import CharacterController

# 初始化
cap = cv2.VideoCapture(0)
segmentor = Segmentor()
pose_estimator = PoseEstimator()

# 背景圖
bg_image = cv2.imread("bg.jpg")
if bg_image is None:
    bg_image = np.zeros((480, 640, 3), dtype=np.uint8)
    bg_image[:] = (100, 200, 255)

# 畫面大小
canvas_h, canvas_w = bg_image.shape[:2]
controller = CharacterController(canvas_width=canvas_w, canvas_height=canvas_h, scale=0.3)

# 狀態旗標
game_started = False
countdown_started = False
countdown_start_time = None

# 遊戲主迴圈
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w = frame.shape[:2]
    bg_resized = cv2.resize(bg_image, (w, h))

    # ---- Step 1. 偵測 Hi 起手 ----
    action = pose_estimator.detect_pose(frame)

    # ---- Step 2. Segmentation + 擷取人物 ----
    mask = segmentor.get_mask(frame)
    fg_rgba = extract_foreground(frame, mask)
    fg_small = resize_foreground(fg_rgba, scale=controller.scale)

    # 初始化人物尺寸，並以原始人物中心 x 軸為初始位置
    if controller.char_width == 100:
        fg_h, fg_w = fg_small.shape[:2]

        # 根據 segmentation 找出人物 x 軸中心
        gray_mask = cv2.cvtColor(fg_rgba, cv2.COLOR_BGRA2GRAY)
        x_indices = np.where(gray_mask > 10)[1]  # 取得非透明區域的 x 座標
        if len(x_indices) > 0:
            initial_center_x = int(np.mean(x_indices))
        else:
            initial_center_x = w // 2

        controller.set_character_size(fg_w, fg_h, initial_center_x=initial_center_x)

    # 建立畫面
    canvas = bg_resized.copy()

    # Step 3. 等待 Hi 起手
    if not game_started:
        canvas = overlay_on_background(canvas, fg_small, position='bottom_center')

        if action == 'hi' and not countdown_started:
            countdown_started = True
            countdown_start_time = time.time()

        if countdown_started:
            elapsed = time.time() - countdown_start_time
            remaining = 3 - int(elapsed)

            if remaining > 0:
                cv2.putText(canvas, f"Starting in {remaining}", (180, 240),
                            cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 50, 255), 5)
            else:
                game_started = True

        else:
            cv2.putText(canvas, "Raise your hand to start (Hi!)", (70, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # ---- Step 4. 正式開始遊戲（控制人物） ----
    else:
        controller.update(action)
        pos = controller.get_position()
        canvas = overlay_on_background(canvas, fg_small, position=pos)
        cv2.putText(canvas, f"Pose: {action}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)

    # 顯示畫面
    cv2.imshow("Game Pose Control", canvas)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
'''