import time
import random
import numpy as np
from mss import mss
from ultralytics import YOLO
import pyautogui
import pygetwindow as gw
from pynput import mouse, keyboard

MODEL_PATH = "./runs/detect/train2/weights/best.pt"
MINE_CLASSES = {"mine_ii", "mine_iii"}
MINE_WAIT_SEC = 10
WALK_WAIT_RANGE = (3.0, 5.0)
CONF_THRESHOLD = 0.25

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

model = YOLO(MODEL_PATH)
print(f"✅ 已載入模型: {MODEL_PATH}")

window = gw.getWindowsWithTitle("Albion Online Client")[0]
region = {
    "top": window.top,
    "left": window.left,
    "width": window.width,
    "height": window.height,
}
print("🎮 偵測範圍:", region)

sct = mss()


def wait_for_click():
    print("📍 請在 3 秒後，用滑鼠左鍵點一下主角位置以記錄座標…")
    time.sleep(4)
    pos = []

    def on_click(x, y, button, pressed):
        if pressed and button.name == "left":
            pos.append((x, y))
            print(f"✅ 已記錄主角位置: {x}, {y}")
            return False

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    return pos[0]


def click_left(xy, dur=0.1):
    pyautogui.moveTo(xy[0], xy[1], duration=dur)
    pyautogui.click(button="left")


def random_walk(region):
    x = random.randint(region["left"] + 100, region["left"] + region["width"] - 100)
    y = random.randint(region["top"] + 100, region["top"] + region["height"] - 100)
    print(f"🚶 隨機走到: ({x}, {y})")
    click_left((x, y))
    time.sleep(random.uniform(*WALK_WAIT_RANGE))


def grab_frame():
    sct_img = sct.grab(region)
    return np.array(sct_img)[:, :, :3]


def press_A():
    """模擬按下鍵盤 A 鍵上馬，然後等待 3 秒"""
    print("🐎 按下 A 上馬中...")
    ctrl = keyboard.Controller()
    ctrl.press("a")
    time.sleep(0.1)
    ctrl.release("a")
    time.sleep(3)
    print("✅ 上馬完成，繼續任務。")


print("⚒️ 開始自動採礦任務 (Ctrl+C 結束)")
time.sleep(1.5)

while True:
    frame = grab_frame()
    results = model.predict(source=frame, conf=CONF_THRESHOLD, verbose=False)
    boxes = results[0].boxes

    target_center = None
    target_name = None

    for box in boxes:
        cls_idx = int(box.cls[0])
        cls_name = model.names.get(cls_idx, str(cls_idx))
        if cls_name in MINE_CLASSES:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cx = region["left"] + (x1 + x2) // 2
            cy = region["top"] + (y1 + y2) // 2
            target_center = (cx, cy)
            target_name = cls_name
            break

    if target_center:
        print(f"🪓 發現礦物 {target_name}，位置: {target_center} → 左鍵點擊採集")
        click_left(target_center)
        time.sleep(MINE_WAIT_SEC)
        press_A()
    else:
        print("🔍 未發現礦物 → 隨機走動探索…")
        random_walk(region)
