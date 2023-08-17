from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get('https://www.zhihu.com/')
time.sleep(3) #等待3秒
js='window.open("https://mail.163.com");'
driver.execute_script(js)
driver.maximize_window()

#driver.set_window_size(480, 800)  # width 400, height 800
# 使用 id 属性来定位输入框
title = driver.title  # 获取网页的title
url = driver.current_url
size = driver.get_window_size()
driver.refresh()
print(title)
print(url)
print(size)
time.sleep(5)
driver.close()
#driver.quit()
