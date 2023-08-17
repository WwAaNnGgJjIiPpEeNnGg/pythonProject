from selenium import webdriver
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

browser = webdriver.Chrome(ChromeDriverManager().install())

# 创建一个 Chrome 浏览器实例
browser = webdriver.Chrome()

# 打开 Google 搜索页面
browser.get('https://www.baidu.com')

# 在搜索框中输入“今日天气”
search_box = browser.find_element_by_name('q')
search_box.send_keys('今日天气')
search_box.submit()

# 等待 10 秒钟
time.sleep(10)

# 关闭浏览器
browser.quit()
