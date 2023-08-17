import tkinter as tk
from tkinter import ttk


def calculate():
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        result.set(num1 + num2)
    except ValueError:
        result.set("Invalid input")


# 创建主窗口
root = tk.Tk()
root.title("简单计算器")

# 创建输入框和标签
label_num1 = ttk.Label(root, text="数值1:")
label_num1.pack()
entry_num1 = ttk.Entry(root)
entry_num1.pack()

label_num2 = ttk.Label(root, text="数值2:")
label_num2.pack()
entry_num2 = ttk.Entry(root)
entry_num2.pack()

# 创建计算按钮
calculate_button = ttk.Button(root, text="计算", command=calculate)
calculate_button.pack()

# 创建结果标签
result = tk.StringVar()
result_label = ttk.Label(root, textvariable=result)
result_label.pack()

# 运行主循环
root.mainloop()
