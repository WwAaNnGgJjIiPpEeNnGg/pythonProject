import driver as driver
import ele as ele
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
driver.lock(5)
driver = webdriver.Remote()
action = TouchAction(driver)  # 创建 TouchAction 对象
# 在坐标(10,100) 位置按下，等待100ms，滑动到 ele 元素上释放
action.press(x=10, y=100).wait(100).move_to(el=ele).release()
# 执行动作
action.perform()
