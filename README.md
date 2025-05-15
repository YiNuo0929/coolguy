# Pose-Based Virtual Character Control System

本專案為一個基於 Mediapipe 與 OpenCV 的即時人體姿勢控制系統，透過攝影機偵測人體動作，控制畫面中的虛擬小人進行左右移動與跳躍等操作。專案採模組化設計，後續可擴充角色動畫、多人控制、遊戲邏輯等功能。

## 📁 專案結構

├── main.py                    # 整合各模組進行流程控制

├── segmentor.py               # 使用 Mediapipe 進行人像分割

├── pose_estimator.py          # 使用 Mediapipe Pose 偵測人體動作（含 hi/left/right/jump）

├── game_overlay.py            # 貼圖模組，負責人物裁切、縮小與疊加到背景

├── character_controller.py    # 控制小人位置與跳躍/左右移動行為

## 📌 各模組說明

### `main.py`
- 主控制流程
- 負責攝影機畫面讀取、初始化模組
- 分為兩階段：
  1. **啟動階段**：等待使用者比出「hi」手勢，啟動倒數三秒後開始遊戲
  2. **遊戲階段**：開始透過姿勢偵測控制小人左右移動與跳躍
- 初始化時小人會出現在畫面下方中央

### `segmentor.py`
- 封裝 Mediapipe 的 `SelfieSegmentation`
- 輸入攝影機畫面，輸出布林值遮罩（人物區域）

### `pose_estimator.py`
- 使用 Mediapipe Pose 模型分析人體姿勢
- 回傳動作標籤：`left`、`right`、`jump`、`hi`、`neutral`
- 可用於遊戲邏輯觸發，例如開始遊戲、控制方向與跳躍
- 一開始要比hi遊戲才會進行

### `game_overlay.py`
- 將裁切後的前景（人物）貼到背景圖上
- 支援縮小比例與自訂貼圖位置 `(x, y)`
- 提供：
  - `extract_foreground()`
  - `resize_foreground()`
  - `overlay_on_background()`

### `character_controller.py`
- 管理虛擬小人的狀態與位置邏輯
- 功能包含：
  - x/y 位置控制
  - 跳躍模擬（簡易重力）
  - 左右移動速度設定
  - 自動限制邊界（不跑出畫面）
  - 根據動作更新人物位置

## 目前實作完成狀態

-  使用 Mediapipe Pose 偵測人物動作
- 使用 Mediapipe SelfieSegmentation 擷取人物並縮小貼圖
- 小人可根據 `left`、`right`、`jump` 動作做對應移動(我不太確定是否成功因為我沒辦法測試)

## 🚧 目前開發進度與卡點
- 姿勢的判定不確定好不好
- 開場前定位人物站立中心點，並將其作為虛擬角色初始位置基準，這個我還沒有很確定要怎麼實作
- 加入xy軸定位後（因為要做人物移動），一開始人物變得沒辦法在中間地板

## 💻 執行方式

```bash
python main.py
