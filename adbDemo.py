import os
import subprocess
# 安装apk文件
def install_apk(device, apk_file):
    command = f'adb -s {device} install -r {apk_file}'
    os.system(command)

# 卸载apk包
def uninstall_apk(device, package_name):
    command = f'adb -s {device} uninstall {package_name}'
    os.system(command)

# 显示所有已连接设备
def list_devices():
    devices = []
    result = os.popen('adb devices').readlines()
    for item in result:
        if '\tdevice' in item:
            devices.append(item.split('\t')[0])
    return devices

# 显示已安装的全部应用程序
def list_packages(device):
    packages = []
    result = os.popen(f'adb -s {device} shell pm list packages ').readlines()
    for item in result:
        packages.append(item.strip().split(':')[1])
    return packages
# 显示已安装的第三方应用程序
def list_packages3(device):
    packages3 = []
    result =os.popen(f'adb -s {device} shell pm list packages -3').readlines()
    for item in result:
        packages3.append(item.strip().split(':')[1])
    return packages3
# 将文件推送到设备上 /sdcard
def push_file(device,local_file_path,remote_file_path):
    #command = f'adb -s device push {local_file_path} {remote_file_path}'
    #os.system(command)
    # 使用adb命令将本地文件推送到设备
    subprocess.run(["adb", "-s", device, "push", local_file_path, remote_file_path])
# 将文件从手机端拉取到电脑端
def pull_file(device,phone_file_path,pc_file_oath):
    subprocess.run((["adb", "-s", device, "pull", phone_file_path, pc_file_oath]))
    #command = "{adb} {-s} pull".format(device, phone_file_path, pc_file_oath)
    #os.system(command)

# 拉取手机端日志
#def get_phonelogs(device,logcat):
# 主程序
def main():
    devices = list_devices()
    if not devices:
        print('未发现设备，请连接设备并启用调试模式。')
        return
    print('可用设备：')
    for i, device in enumerate(devices):
        print(f'{i + 1}. {device}')
    choice = input('请选择设备编号：')
    if not choice:
        print("请确认设备编号！")
    device = devices[int(choice) - 1]
    print(f'已选择设备：{device}')
    while True:
        print('请选择操作：')
        print('1. 安装应用程序')
        print('2. 卸载应用程序')
        print('3. 显示全部已安装应用程序列表')
        print('4. 显示已安装的第三方应用程序')
        print('5. 推送文件到手机端 /sdcard')
        print('6. 拉取手机端文件到Pc')
        print('7. 退出')
        choice = input()
        if choice == '1':
            apk_file = input('请输入APK文件路径：')
            install_apk(device, apk_file)
        elif choice == '2':
            package_name = input('请输入应用程序包名：')
            uninstall_apk(device, package_name)
        elif choice == '3':
            packages = list_packages(device)
            if not packages:
                print('未安装应用程序。')
            else:
                print('已安装的全部应用程序列表：')
                for i, package in enumerate(packages):
                    print(f'{i + 1}. {package}')
        elif choice == '4':
            packages3 = list_packages3(device)
            if not packages3:
                print('未安装应用程序。')
            else:
                print('已安装的第三方应用程序列表：')
                for i, package in enumerate(packages3):
                    print(f'{i + 1}. {package}')
        elif choice == '5':
            # 获取本地文件路径
            local_file_path = input("请输入本地文件路径：")
            if not os.path.exists(local_file_path):
                print("文件不存在")
                return
                # 推送文件到设备
            remote_file_path = "/sdcard/" + os.path.basename(local_file_path)
            push_file(device, local_file_path, remote_file_path)
            print(f"已将文件推送到设备 {device}")
        elif choice == '6':
            # 获取手机文件路径
            phone_file_path = input("请输入手机文件路径：")
            if not os.path.exists(phone_file_path):
                print("文件不存在")
                return
                # 拉取文件到PC端
            pc_file_path = "/D" + os.path.basename(phone_file_path)
            pull_file(device, phone_file_path, pc_file_path)
            print(f"已将文件拉取到到Pc")
        elif choice == '7':
            break
        else:
            print('无效选择，请重新输入。')

if __name__ == '__main__':
    main()
