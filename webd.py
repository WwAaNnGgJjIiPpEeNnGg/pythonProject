import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver

# 设置浏览器选项
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # 隐藏浏览器窗口

# 创建浏览器对象
browser = webdriver.Chrome(options=options)

# 访问 Google 首页
url = 'https://www.google.com'
browser.get(url)

# 等待搜索框元素加载出来
wait = WebDriverWait(browser, 10)
search_box = wait.until(EC.presence_of_element_located((By.NAME, 'q')))

# 在搜索框中输入关键词并搜索
search_box.send_keys('今天天气 ')
search_box.submit()

# 等待10S
time.sleep(10)

# 关闭浏览器
browser.quit()
