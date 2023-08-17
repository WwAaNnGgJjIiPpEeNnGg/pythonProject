import pyautogui
import time

# 等待一些时间以便你切换到你想要点击的应用窗口
time.sleep(5)

# 切换到目标应用程序（示例：Windows下Alt+Tab切换）
pyautogui.hotkey('alt', 'tab')
time.sleep(1)  # 等待切换完成

# 定义要点击的坐标点的x和y值
x_coordinate = 400
y_coordinate = 400

# 循环点击
try:
    while True:
        pyautogui.click(x=x_coordinate, y=y_coordinate)
        time.sleep(1)  # 等待1秒再进行下一次点击
except KeyboardInterrupt:
    print("脚本已停止")

   # import pyautogui

    # 获取当前鼠标的坐标点
x, y = pyautogui.position()

# 输出鼠标坐标
print(f"当前鼠标坐标：X = {x}, Y = {y}")
