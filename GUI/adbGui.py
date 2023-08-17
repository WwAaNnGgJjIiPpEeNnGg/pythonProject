import tkinter as tk
from tkinter import ttk, simpledialog
import os
import subprocess
import sys
import threading
from tkinter import filedialog
import time


class ADBToolGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ADB Tool")
        self.device_var = tk.StringVar()
        self.log_var = tk.StringVar()
        self.create_widgets()

    # 创建按钮
    def create_widgets(self):
        row_index = 0
        ttk.Label(self.root, text="选择设备：").grid(row=row_index, column=0, padx=5, pady=5, sticky="w")
        self.device_combo = ttk.Combobox(self.root, textvariable=self.device_var)
        self.device_combo.grid(row=row_index, column=1, padx=5, pady=5, sticky="w")

        row_index += 1
        ttk.Button(self.root, text="连接设备", command=self.connect_device).grid(row=row_index, column=0, padx=5,
                                                                                 pady=5, sticky="w")
        ttk.Button(self.root, text="断开设备", command=self.disconnect_device).grid(row=row_index, column=1, padx=5,
                                                                                    pady=5, sticky="w")

        row_index += 1
        ttk.Button(self.root, text="开始日志", command=self.start_logcat).grid(row=row_index, column=0, padx=5, pady=5,
                                                                               sticky="w")
        ttk.Button(self.root, text="停止日志", command=self.stop_logcat).grid(row=row_index, column=1, padx=5, pady=5,
                                                                              sticky="w")

        row_index += 1
        ttk.Button(self.root, text="显示设备详情", command=self.show_device_info).grid(row=row_index, column=0, padx=5,
                                                                                       pady=5, sticky="w")
        ttk.Button(self.root, text="查看设备分辨率", command=self.show_resolution).grid(row=row_index, column=1, padx=5,
                                                                                        pady=5, sticky="w")

        row_index += 1
        ttk.Button(self.root, text="安装应用", command=self.install_apk).grid(row=row_index, column=1, padx=5, pady=5,
                                                                              sticky="w")
        ttk.Button(self.root, text="卸载应用", command=self.uninstall_apk).grid(row=row_index, column=0, padx=5, pady=5,
                                                                                sticky="w")

        row_index += 1
        ttk.Button(self.root, text="显示第三方应用", command=self.show_third_party_apps).grid(row=row_index, column=0,
                                                                                              padx=5, pady=5,
                                                                                              sticky="w")
        ttk.Button(self.root, text="显示已安装应用", command=self.show_installed_apps).grid(row=row_index, column=1,
                                                                                            padx=5, pady=5, sticky="w")

        row_index += 1
        ttk.Button(self.root, text="拉取文件到 PC ", command=self.pull_file).grid(row=row_index, column=0, padx=5,
                                                                                  pady=5, sticky="w")
        ttk.Button(self.root, text="推送文件到设备", command=self.push_file).grid(row=row_index, column=1, padx=5,
                                                                                  pady=5, sticky="w")

        row_index += 1
        ttk.Label(self.root, text="操作日志：").grid(row=row_index, column=0, padx=5, pady=5, sticky="w")
        self.log_text = tk.Text(self.root, height=10, wrap=tk.WORD, state=tk.DISABLED)
        self.log_text.grid(row=row_index, column=1, padx=5, pady=5, sticky="w")

    # 连接设备
    def connect_device(self):
        devices = self.list_devices()
        serial_number = self.device_var.get()

        if not devices:
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, "请选择连接设备！\n")
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)
        elif serial_number == "KXU0221301006068":
            device_model = "华为P40"
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, f"设备{device_model}连接成功！\n")
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)
        else:
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, "设备已连接！\n")
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)

        self.device_combo['values'] = devices

    # 断开连接
    def disconnect_device(self):
        serial_number = self.device_var.get()

        if serial_number == "KXU0221301006068":
            device_model = "华为P40"
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, f"设备{device_model}已断开连接！\n")
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)
        else:
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, "当前设备已断开连接！\n")
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)

        self.device_var.set("")
        self.device_combo['values'] = []

    # 开始日志拉取
    def start_logcat(self):
        self.log_thread = threading.Thread(target=self.run_logcat)
        self.log_thread.start()

    # 停止日志拉取
    def stop_logcat(self):
        self.stop_log = True
        self.root.after(100, self.check_log_thread)

    # 判断日志线程是否停止
    def check_log_thread(self):
        if self.log_thread.is_alive():
            self.root.after(100, self.check_log_thread)
        else:
            self.log_thread.join()

    # 拉取日志
    def run_logcat(self):
        self.stop_log = False
        device = self.device_var.get()
        process = subprocess.Popen(['adb', '-s', device, 'logcat'], stdout=subprocess.PIPE, universal_newlines=True)

        while not self.stop_log:
            line = process.stdout.readline()
            if not line:
                break
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, line)
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)

        process.stdout.close()

    # 显示设备详情
    # def show_device_info(self):
    #    device = self.device_var.get()
    #    result = self.run_command(f'adb -s {device} shell dumpsys battery')
    #    self.log_text.config(state=tk.NORMAL)
    #    self.log_text.insert(tk.END, result)
    #    self.log_text.see(tk.END)
    #    self.log_text.config(state=tk.DISABLED)
    def show_device_info(self):
        device = self.device_var.get()
        result = self.run_command(f'adb -s {device} shell dumpsys battery')
        translated_result = self.translate_to_chinese(result)

        # 输出翻译后的结果到操作日志
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, translated_result)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    # 翻译
    def translate_to_chinese(self, text):
        translation_dict = {
            'Current Battery Service state:': '当前电池状态:',
            'AC powered:': '交流供电:',
            'USB powered:': 'USB供电:',
            'Wireless powered:': '无线供电:',
            'Max charging current:': '最大充电电流:',
            'Max charging voltage:': '最大充电电压:',
            'Charge counter:': '充电计数:',
            'status:': '状态:',
            'health:': '健康状态:',
            'present:': '电池是否存在:',
            'level:': '电量:',
            'scale:': '电量刻度:',
            'voltage:': '电压:',
            'temperature:': '温度:',
            'technology:': '电池技术:',
            'Li-poly': '锂聚合物'
            # 可以继续添加更多翻译
        }

        translated_lines = []
        for line in text.split('\n'):
            for eng, chi in translation_dict.items():
                if eng in line:
                    line = line.replace(eng, chi)
            translated_lines.append(line)

        return '\n'.join(translated_lines)

    # 安装apk
    def install_apk(self):
        # 获取设备和APK文件路径
        device = self.device_var.get()
        apk_file = self.get_file_path("请选择APK文件")

        if not apk_file:
            return  # 如果用户没有选择文件，直接返回

        # 检查文件扩展名是否为.apk
        if not apk_file.lower().endswith('.apk'):
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, "请选择.apk文件\n")
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)
            return

        # 创建一个新线程来执行安装操作
        install_thread = threading.Thread(target=self.run_install, args=(device, apk_file))
        install_thread.start()

    def run_install(self, device, apk_file):
        # 在开始安装前插入一个正在安装中的提示
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, "正在安装中...\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

        # 记录安装开始时间
        start_time = time.time()

        command = ['adb', '-s', device, 'install', '-r', apk_file]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,
                                encoding='utf-8')

        # 计算安装耗时
        end_time = time.time()
        elapsed_time = end_time - start_time

        # 将安装结果和耗时信息替换正在安装中的提示
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("end -2l", tk.END)  # 删除最后两行（正在安装中和空行）
        self.log_text.insert(tk.END, result.stdout)
        self.log_text.insert(tk.END, result.stderr)
        self.log_text.insert(tk.END, f"安装耗时：{elapsed_time:.2f}秒\n")  # 输出耗时
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

        # 如果设备序列号符合，执行自动化点击操作
        if device == "JFPF85PZ4HWKMNQK":
            self.perform_auto_install(device)

        #if device == "kjo7eqwkskhm5lvo":
        #    self.perform_auto_install1(device)

    def perform_auto_install(self, device):
        # 自动化点击，假设坐标为 (140, 756)
        time.sleep(1)  # 等待1秒
        subprocess.run(['adb', '-s', device, 'shell', 'input', 'tap', '140', '756'])
        # 输入密码 "wgame123"，假设坐标为 (140, 756)
        subprocess.run(['adb', '-s', device, 'shell', 'input', 'text', 'wgame123'])
        # 模拟点击安装按钮，假设坐标为 (757, 1021)
        subprocess.run(['adb', '-s', device, 'shell', 'input', 'tap', '757', '1021'])
        # 模拟点击安装按钮，假设坐标为 (502, 2165)
        time.sleep(5)
        subprocess.run(['adb', '-s', device, 'shell', 'input', 'tap', '502', '2165'])

    # def perform_auto_install1(self, device):
     #   # 自动化点击，假设坐标为 (256, 2228)
      #  time.sleep(1)  # 等待1秒
      #  subprocess.run(['adb', '-s', device, 'shell', 'input', 'tap', '256', '2228'])

    # 卸载apk
    def uninstall_apk(self):
        device = self.device_var.get()
        package_name = self.get_input("请输入应用程序包名")
        if package_name:
            result = self.run_command(f'adb -s {device} uninstall {package_name}')
            if "Failure" in result:  # 判断是否包含 "Failure" 字样
                self.log_text.config(state=tk.NORMAL)
                self.log_text.insert(tk.END, "请输入正确的包名！\n")
                self.log_text.see(tk.END)
                self.log_text.config(state=tk.DISABLED)
            else:
                self.log_text.config(state=tk.NORMAL)
                self.log_text.insert(tk.END, result)
                self.log_text.see(tk.END)
                self.log_text.config(state=tk.DISABLED)

    # 显示所有已安装应用
    def show_installed_apps(self):
        device = self.device_var.get()
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        process = subprocess.Popen(['adb', '-s', device, 'shell', 'pm', 'list', 'packages'], stdout=subprocess.PIPE,
                                   universal_newlines=True)
        for line in process.stdout:
            self.log_text.insert(tk.END, line)
            self.log_text.see(tk.END)
        process.stdout.close()
        self.log_text.config(state=tk.DISABLED)

    # 只显示第三方已安装应用
    def show_third_party_apps(self):
        device = self.device_var.get()
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        process = subprocess.Popen(['adb', '-s', device, 'shell', 'pm', 'list', 'packages', '-3'],
                                   stdout=subprocess.PIPE, universal_newlines=True)
        for line in process.stdout:
            self.log_text.insert(tk.END, line)
            self.log_text.see(tk.END)
        process.stdout.close()
        self.log_text.config(state=tk.DISABLED)

    # 推送文件到设备
    def push_file(self):
        device = self.device_var.get()
        local_file_path = self.get_file_path("请选择要推送的文件")
        if local_file_path:
            remote_folder_path = self.get_input("请输入远程文件夹路径（不包含文件名）")
            if remote_folder_path is None:  # 用户取消了远程文件夹路径的选择
                return  # 不执行后续操作

            remote_file_name = os.path.basename(local_file_path)
            remote_file_path = remote_folder_path + '/' + remote_file_name

            # 在操作日志中输出提示
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, "正在推送文件中...\n")
            self.log_text.see(tk.END)
            self.log_text.update_idletasks()  # 更新界面
            self.log_text.config(state=tk.DISABLED)

            start_time = time.time()  # 记录推送开始时间

            # 创建一个新线程来执行推送操作
            push_thread = threading.Thread(target=self.run_push_file,
                                           args=(device, local_file_path, remote_file_path, start_time))
            push_thread.start()

    def run_push_file(self, device, local_file_path, remote_file_path, start_time):
        command = ['adb', '-s', device, 'push', local_file_path, remote_file_path]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True,
                                encoding='utf-8')

        stdout = result.stdout if result.stdout else ""
        stderr = result.stderr if result.stderr else ""
        output = stdout + stderr

        end_time = time.time()  # 记录推送结束时间
        elapsed_time = end_time - start_time  # 计算推送耗时

        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)  # 清空之前的提示
        self.log_text.insert(tk.END, output)
        self.log_text.insert(tk.END, f"文件推送成功！耗时：{elapsed_time:.2f}秒\n")  # 输出推送成功和耗时信息
        self.log_text.see(tk.END)
        self.log_text.update_idletasks()  # 更新界面
        self.log_text.config(state=tk.DISABLED)

    # 拉取文件到PC
    def pull_file(self):
        device = self.device_var.get()
        remote_file_path = self.get_input("请输入要拉取的设备文件路径")
        if remote_file_path:
            local_folder_path = self.get_input("请输入本地文件夹路径，将文件保存在该路径下")
            if local_folder_path:
                local_folder_path = os.path.normpath(local_folder_path)  # 规范化路径

                # 将 Unicode 路径转换为本地系统编码
                local_folder_path_encoded = local_folder_path.encode(sys.getfilesystemencoding()).decode('utf-8')

                command = f'adb -s {device} pull "{remote_file_path}" "{local_folder_path_encoded}"'
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

                stdout = result.stdout if result.stdout else b""
                stderr = result.stderr if result.stderr else b""
                output = stdout + stderr

                self.log_text.config(state=tk.NORMAL)
                self.log_text.delete(1.0, tk.END)  # 清空日志文本框
                self.log_text.insert(tk.END, output.decode('utf-8', errors='replace'))
                self.log_text.update_idletasks()  # 更新界面
                self.log_text.config(state=tk.DISABLED)

    # 输出设备分辨率
    def show_resolution(self):
        device = self.device_var.get()
        result = self.run_command(f'adb -s {device} shell wm size')

        # 将设备分辨率信息添加到操作日志
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, result + '\n')
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def get_input(self, prompt):
        return simpledialog.askstring("输入", prompt, parent=self.root)

    def get_file_path(self, prompt):
        return filedialog.askopenfilename(title=prompt, parent=self.root)

    def list_devices(self):
        devices = []
        result = subprocess.getoutput('adb devices')
        lines = result.strip().split('\n')
        for line in lines[1:]:
            device = line.split('\t')[0]
            devices.append(device)
        return devices

    def run_command(self, command):
        result = subprocess.getoutput(command)
        return result


def main():
    root = tk.Tk()
    app = ADBToolGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
