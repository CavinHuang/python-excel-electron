import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, font
from tax_model.test import process_excel
import os
import logging
import threading

# 定义一个用于重定向标准输出的辅助类
class TextHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.see(tk.END)  # 滚动到文本末尾


# 创建窗口
window = tk.Tk()
window.title("Excel英国关税自动化工具")

# 设置字体
chinese_font = font.Font(family='微软雅黑', size=12)
window.option_add("*Font", chinese_font)

# 设置窗口大小和位置
window_width = 600
window_height = 350
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# 创建选择结果标签
result_label = tk.Label(window, text="")
result_label.pack()

# 记录选择的文件路径
selected_file_path = ""

# 新增：创建文本控件用于显示日志
log_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=80, height=10)
log_text.pack(padx=20)

# 创建选择文件函数
def open_file_dialog():
    global selected_file_path
    selected_file_path = ''
    # 清空之前的记录
    log_text.delete('1.0', tk.END)
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        file_name = os.path.basename(file_path)  # 获取文件名
        result_label.config(text="当前选择的文件：" + file_name)
        selected_file_path = file_path
    else:
        result_label.config(text="")
        selected_file_path = ''

# 创建开始数据操作函数
def start_data_processing():
    global selected_file_path
    if not selected_file_path:
        messagebox.showinfo("提示", "请先选择一个文件")
        return

    # 清空日志文本控件
    log_text.delete('1.0', tk.END)

    # 将日志处理器添加到根日志
    text_handler = TextHandler(log_text)
    root_logger = logging.getLogger('log')
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(text_handler)

    # 调用数据处理函数
    # data_processor.process_excel(selected_file_path)
    # 启动数据处理的工作线程
    def process_data():
        process_excel(selected_file_path)
        result_label.config(text="数据操作完成")
        # selected_file_path = ""

    processing_thread = threading.Thread(target=process_data)
    processing_thread.start()

    # 移除日志处理器
    # root_logger.removeHandler(text_handler)

# 创建按钮
open_button = tk.Button(window, text="选择Excel文件", command=open_file_dialog)
start_button = tk.Button(window, text="开始", command=start_data_processing)

# 布局
open_button.pack(pady=10)
start_button.pack(pady=10)

# 进入主循环
window.mainloop()
