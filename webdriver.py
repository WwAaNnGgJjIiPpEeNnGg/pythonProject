import time

from selenium import webdriver

# 设置浏览器选项
options = webdriver.ChromeOptions()
#options.add_argument('--headless')  # 隐藏浏览器窗口

# 创建浏览器对象
browser = webdriver.Chrome(options=options)

# 访问 Google 首页
url = 'https://www.google.com/'
browser.get(url)
# 等待页面加载
time.sleep(10)

# 在搜索框中输入关键词并搜索
search_box = browser.find_element_by_name('q')
search_box.send_keys('1')
search_box.submit()


# 等待10秒钟
time.sleep(10)

# 关闭浏览器
browser.quit()