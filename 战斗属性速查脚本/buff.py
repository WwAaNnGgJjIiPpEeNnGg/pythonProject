import os
import re
import csv
import tkinter as tk
from tkinter import filedialog
from prettytable import PrettyTable

from 战斗属性速查脚本.战斗属性速查 import matches

# 创建Tkinter应用程序窗口
app = tk.Tk()
app.title("数据可视化程序")

def open_file():
    # 打开文件对话框并获取选择的文件路径
    file_path = filedialog.askopenfilename()

    if file_path:
        process_file(file_path)

def process_file(file_path):
    with open(file_path, 'r') as f:
        data = f.read()

    # ... 剩余的代码，与您提供的代码保持一致 ...

    if matches:
            # ... 剩余的代码，与您提供的代码保持一致 ...
    else:
        result_label.config(text="未匹配到数据")

# 创建打开文件按钮
open_button = tk.Button(app, text="选择文件", command=open_file)
open_button.pack(pady=10)

# 创建一个标签来显示处理结果
result_label = tk.Label(app, text="", fg="red")
result_label.pack()

# 启动Tkinter事件循环
app.mainloop()
