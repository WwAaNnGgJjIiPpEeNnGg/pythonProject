import os

# 输入APK文件路径
apk_path = input("请输入APK文件的路径：")

# 确保APK文件存在
if not os.path.isfile(apk_path):
    print("错误：文件不存在！")
    exit()
#print("adb devices")
# 安装APK文件
os.system("adb install " + apk_path)
