import subprocess
import tkinter as tk
from tkinter import ttk
import os
import subprocess


def list_devices():
    devices = []
    result = os.popen('adb devices').readlines()
    for item in result:
        if '\tdevice' in item:
            devices.append(item.split('\t')[0])
    return devices


def install_apk(device, apk_file):
    command = f'adb -s {device} install -r {apk_file}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    progress_window = tk.Tk()
    progress_window.title('APK Installation Progress')

    progress_bar = ttk.Progressbar(progress_window, mode='determinate', maximum=100)
    progress_bar.pack(pady=10)

    def update_progress():
        output = process.stdout.readline()
        if output:
            # Update progress bar based on the adb command output
            # Assuming the adb command prints the installation progress as a percentage
            try:
                progress = float(output.strip().decode('utf-8').split()[1].strip('%'))
            except ValueError:
                print("Error: Could not convert progress value to float.")
            # progress = float(output.strip().decode('utf-8').split()[1].strip('%'))
            progress_bar['value'] = progress
            progress_window.after(100, update_progress)
        elif process.poll() is not None:
            # Installation completed or an error occurred
            progress_window.destroy()

    update_progress()
    progress_window.mainloop()


def main():
    devices = list_devices()
    if not devices:
        print('未发现设备，请连接设备并启用调试模式。')
        return
    print('可用设备：')
    for i, device in enumerate(devices):
        print(f'{i + 1}. {device}')
        if device == 'KXU0221301006068':
            print(device + '\t华为：P40')
    choice = input('请选择设备编号：')
    if not choice:
        print("请确认设备编号！")
    device = devices[int(choice) - 1]

    print(f'已选择设备：{device}')
    while True:
        print('请选择操作：')
        print('1. 显示设备详情')
        print('2. 安装应用程序')
        print('3. 退出')
        # try:
        #     choice = input()
        # except KeyboardInterrupt:
        choice = input()
        if choice == '1':
            print("设备信息如下：")

        elif choice == '2':
            apk_file = input('请输入APK文件路径：')
            install_apk(device, apk_file)
        elif choice == '3':
            break
        else:
            print('无效选择，请重新输入。')


if __name__ == '__main__':
    main()

# Usage example
# install_apk('device_id', 'path/to/apk_file.apk')
