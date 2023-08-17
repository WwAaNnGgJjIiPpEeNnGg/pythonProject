import pyautogui
import time

# 获取屏幕大小
screenWidth, screenHeight = pyautogui.size()

# 设置鼠标移动的相对位置
xOffset = 50
yOffset = 50

# 将鼠标移动到指定位置
pyautogui.moveTo(xOffset, yOffset, duration=1)

# 记录原始位置
originalX, originalY = pyautogui.position()

# 进入循环，如果鼠标位置发生变化则退出循环
while True:
    currentX, currentY = pyautogui.position()
    if currentX != originalX or currentY != originalY:
        break
    time.sleep(0.1)
    pyautogui.moveTo(originalX, originalY, duration=1)

# 将鼠标移回原始位置

