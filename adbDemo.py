import os
import subprocess
from tqdm import tqdm
import sys


# 显示设备详情信息
def dumpsys_battery(device):
    command = f'adb -s {device} shell dumpsys battery'
    os.system(command)


# 安装apk文件  -r 覆盖安装
def install_apk(device, apk_file):
    command = f'adb -s {device} install -r {apk_file}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    with tqdm(total=100, unit='%', ncols=60) as pbar:
        for line in process.stdout:
            # 假设adb命令会打印出百分比的安装进度
            output = line.decode().strip()
            if output.startswith('Success'):
                pbar.update(100)  # 安装成功，进度条到达100%
            elif output.startswith('Failure'):
                # 安装失败，根据需要进行处理
                pbar.close()
                print("安装失败")
                break
            elif output.startswith('Installing'):
                progress = float(output.split()[1].strip('%'))
                pbar.update(progress - pbar.n)  # 更新进度条

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
    result = os.popen(f'adb -s {device} shell pm list packages -3').readlines()
    for item in result:
        packages3.append(item.strip().split(':')[1])
    return packages3


# 将文件推送到设备上 /sdcard
def push_file(device, local_file_path, remote_file_path):
    # command = f'adb -s device push {local_file_path} {remote_file_path}'
    # os.system(command)
    # 使用adb命令将本地文件推送到设备
    subprocess.run(["adb", "-s", device, "push", local_file_path, remote_file_path])


# 将文件从手机端拉取到电脑端
# def pull_file(device, phone_file_path, pc_file_path):
# subprocess.run((["adb", "-s", device, "pull", phone_file_path, pc_file_path]))
# command = "{adb} {-s} pull".format(device, phone_file_path, pc_file_path)
# command = f'adb -s {device} pull {phone_file_path} {pc_file_path}'
# os.system(command)
def pull_file(device, phone_file_path, pc_file_path):
    # 使用subprocess模块执行pull命令
    command = f"adb -s {device} pull {phone_file_path} {pc_file_path}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"{phone_file_path}已成功复制到{pc_file_path}文件夹下 ！！")
    else:
        print("拉取文件失败！请检查文件路径！")
        print(result.stderr)


# 拉取手机端日志
# def get_logs(device,logcat):
# 使用subprocess模块执行adb logcat命令
def run_adb_logcat():
    process = subprocess.Popen(['adb', 'logcat'], stdout=subprocess.PIPE)

    try:
        while True:
            # 检查进程是否已经结束
            if process.poll() is not None:
                break

            # 逐行读取输出
            line = process.stdout.readline()
            if not line:
                break
            # 解码并打印输出，忽略解码错误
            print(line.decode('utf-8', errors='ignore').strip())
    except KeyboardInterrupt:
        # 捕获键盘中断异常
        print("KeyboardInterrupt: Stopping adb logcat...")

    # 等待进程结束
    process.wait()


# 获取设备分辨率
def wm_size(device):
    # 执行 adb shell wm size
    command = f"adb -s {device} shell wm size"
    os.system(command)


# 主程序
def main():
    devices = list_devices()
    if not devices:
        print('未发现设备，请连接设备并启用调试模式。')
        return
    print('可用设备：')
    for i, device in enumerate(devices):
        print(f'{i + 1}. {device}')
        if device == 'MKSBB19314208768':
            print(device + '\t华为：Honor 8c')
        if device == 'KXU0221301006068':
            print(device + '\t华为：P40')
        if device == '2480e012':
            print(device + '\tvivo：Y85a')
    choice = input('请选择设备编号：')
    if not choice:
        print("请确认设备编号！")
    device = devices[int(choice) - 1]

    print(f'已选择设备：{device}')
    while True:
        print('请选择操作：')
        print('1. 显示设备详情')
        print('2. 安装应用程序')
        print('3. 卸载应用程序')
        print('4. 显示全部已安装应用程序列表')
        print('5. 显示已安装的第三方应用程序')
        print('6. 推送backdoor.txt文件到手机端 ')
        print('7. 拉取手机端文件到Pc')
        print('8. 查看当前设备分辨率：')
        print('9. 拉取日志')
        print('10. 退出')
        # try:
        #     choice = input()
        # except KeyboardInterrupt:
        choice = input()
        if choice == '1':
            print("设备信息如下：")
            dumpsys_battery(device)
        elif choice == '2':
            apk_file = input('请输入APK文件路径：')
            install_apk(device, apk_file)
        elif choice == '3':
            package_name = input('请输入应用程序包名：')
            uninstall_apk(device, package_name)
        elif choice == '4':
            packages = list_packages(device)
            if not packages:
                print('未安装应用程序。')
            else:
                print('已安装的全部应用程序列表：')
                for i, package in enumerate(packages):
                    print(f'{i + 1}. {package}')
        elif choice == '5':
            packages3 = list_packages3(device)
            if not packages3:
                print('未安装应用程序。')
            else:
                print('已安装的第三方应用程序列表：')
                for i, package in enumerate(packages3):
                    print(f'{i + 1}. {package}')
        elif choice == '6':
            # 获取本地文件路径
            local_file_path = input("请输入本地文件路径 例如：请输入本地文件路径 例如：C:\\Users\\wangjipeng\\Desktop\\backdoor.txt")
            if not os.path.exists(local_file_path):
                print("文件不存在")
                return
                # 获取设备路径
            remote_file_path = input("请输入设备路径 例如：/sdcard/Android/data/com.wondergames.warpath.gp/files")
            if not remote_file_path.startswith("/"):
                remote_file_path = "/" + remote_file_path

                # 拼接完整的设备路径
            remote_file_path = remote_file_path + "/" + os.path.basename(local_file_path)

            # 推送文件到设备
            push_file(device, local_file_path, remote_file_path)
            print(f"已将文件推送到设备 {device} {remote_file_path} 目录下 ")

            # 推送文件到设备
        # remote_file_path = "/sdcard/" + os.path.basename(local_file_path)
        # push_file(device, local_file_path, remote_file_path)
        # print(f"已将文件推送到设备 {device} /sdcard 目录下 ")
        elif choice == '7':
            # 获取手机文件路径
            # 获取源文件路径和目标文件路径
            phone_file_path = input("请输入要拉取的文件路径（例如：/sdcard/test.txt）：")
            pc_file_path = input("请输入文件保存路径和文件名（例如：D:/test.txt）：")

            # 调用pull_file函数，使用pull命令将手机端文件复制到PC端
            pull_file(device, phone_file_path, pc_file_path)

        elif choice == '8':
            # 获取设备分辨率并输出
            print("当前设备分辨率为：")
            wm_size(device)
        elif choice == '9':
            # 调用函数执行adb logcat
            run_adb_logcat()
        elif choice == '10':
            break
        else:
            print('无效选择，请重新输入。')


if __name__ == '__main__':
    main()
