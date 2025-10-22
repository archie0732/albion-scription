import cv2
import numpy as np
from mss import mss
from ultralytics import YOLO
import pygetwindow as gw
import time

# === 1️⃣ 載入模型 ===
MODEL_PATH = "./runs/detect/train2/weights/best.pt"
model = YOLO(MODEL_PATH)
print(f"✅ 已載入模型: {MODEL_PATH}")

# === 2️⃣ 找遊戲視窗 ===
window = gw.getWindowsWithTitle("Albion Online Client")[0]
region = {
    "top": window.top,
    "left": window.left,
    "width": window.width,
    "height": window.height,
}
print("🎮 偵測範圍:", region)

# === 3️⃣ 初始化擷取器 ===
sct = mss()
cv2.namedWindow("Ore Detection", cv2.WINDOW_NORMAL)  # 可調整大小
cv2.resizeWindow("Ore Detection", 960, 540)  # 初始大小

# === 4️⃣ 主迴圈 ===
fps_time = time.time()
scale = 0.6  # 縮放比例，0.6 = 縮小到 60%
print("📷 開始擷取畫面... (按 Q 結束)")

while True:
    sct_img = sct.grab(region)
    frame = np.array(sct_img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    # YOLO 偵測
    results = model.predict(source=frame, conf=0.25, verbose=False)
    annotated = results[0].plot()

    # 自動縮放畫面（避免太大）
    resized = cv2.resize(annotated, (0, 0), fx=scale, fy=scale)

    # 顯示 FPS
    fps = 1 / (time.time() - fps_time)
    fps_time = time.time()
    cv2.putText(
        resized,
        f"FPS: {fps:.1f}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    # 顯示視窗
    cv2.imshow("Ore Detection", resized)

    # 結束條件
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
print("🛑 已結束礦物偵測。")
