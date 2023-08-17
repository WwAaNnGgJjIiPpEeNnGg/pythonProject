import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import sys


class ADBToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ADB Tool")

        self.device_var = tk.StringVar()

        # 创建按钮
        self.install_button = tk.Button(self.root, text="安装应用", command=self.install_apk)
        self.uninstall_button = tk.Button(self.root, text="卸载应用", command=self.uninstall_apk)
        self.list_packages_button = tk.Button(self.root, text="显示已安装应用", command=self.list_installed_packages)
        self.list_packages3_button = tk.Button(self.root, text="显示第三方应用", command=self.list_third_party_packages)
        self.push_file_button = tk.Button(self.root, text="推送文件到设备", command=self.push_file)
        self.pull_file_button = tk.Button(self.root, text="拉取设备文件到PC", command=self.pull_file)
        self.run_logcat_button = tk.Button(self.root, text="运行日志", command=self.run_adb_logcat)

        # 创建按钮网格布局
        self.install_button.grid(row=0, column=0, padx=10, pady=5)
        self.uninstall_button.grid(row=0, column=1, padx=10, pady=5)
        self.list_packages_button.grid(row=1, column=0, padx=10, pady=5)
        self.list_packages3_button.grid(row=1, column=1, padx=10, pady=5)
        self.push_file_button.grid(row=2, column=0, padx=10, pady=5)
        self.pull_file_button.grid(row=2, column=1, padx=10, pady=5)
        self.run_logcat_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    # 安装应用
    def install_apk(self):
        apk_file = filedialog.askopenfilename(title="请选择APK文件")
        if apk_file:
            device = self.device_var.get()
            command = f'adb -s {device} install -r "{apk_file}"'
            self.run_command(command)

    # 卸载应用
    def uninstall_apk(self):
        package_name = self.get_input("请输入要卸载的应用程序包名")
        if package_name:
            device = self.device_var.get()
            command = f'adb -s {device} uninstall {package_name}'
            self.run_command(command)

    # 显示已安装应用
    def list_installed_packages(self):
        device = self.device_var.get()
        command = f'adb -s {device} shell pm list packages'
        self.run_command(command)

    # 显示第三方应用
    def list_third_party_packages(self):
        device = self.device_var.get()
        command = f'adb -s {device} shell pm list packages -3'
        self.run_command(command)

    # 推送文件到设备
    def push_file(self):
        device = self.device_var.get()
        local_file_path = filedialog.askopenfilename(title="请选择要推送的本地文件")
        if local_file_path:
            remote_file_path = self.get_input("请输入设备路径")
            if remote_file_path:
                command = f'adb -s {device} push "{local_file_path}" "{remote_file_path}"'
                self.run_command(command)

    # 拉取设备文件到PC
    def pull_file(self):
        device = self.device_var.get()
        remote_file_path = self.get_input("请输入要拉取的设备文件路径")
        if remote_file_path:
            local_folder_path = filedialog.askdirectory(title="请选择保存文件的本地文件夹")
            if local_folder_path:
                local_folder_path_encoded = local_folder_path.encode(sys.getfilesystemencoding()).decode('utf-8')
                command = f'adb -s {device} pull "{remote_file_path}" "{local_folder_path_encoded}"'
                self.run_command(command)

    # 运行日志
    def run_adb_logcat(self):
        device = self.device_var.get()
        command = f'adb -s {device} logcat'
        self.run_command(command)

    # 执行命令并显示输出结果
    def run_command(self, command):
        result = subprocess.getoutput(command)
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)  # 清空日志文本框
        self.log_text.insert(tk.END, result)
        self.log_text.update_idletasks()  # 更新界面
        self.log_text.config(state=tk.DISABLED)

    # 获取用户输入
    def get_input(self, prompt):
        return tk.simpledialog.askstring("输入", prompt)


root = tk.Tk()
app = ADBToolGUI(root)
root.mainloop()
