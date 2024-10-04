"""
用于创建一个输入框窗口，以解决傻逼pygame无法输入中文的问题
"""
from tkinter import font
import tkinter as tk
from tkinter import messagebox
import threading
from typing import Any

click_enter = False
def __create_input_box(title: str, option: dict[str, Any]):
    # 创建主窗口
    root = tk.Tk()
    root.title(title)
    click_enter = False
    def on_esc(event):
        """ 当用户按下Esc键时调用此函数 """
        root.destroy()
        return event

    def on_enter(event):
        """ 当用户按下Enter键时调用此函数 """
        global click_enter
        click_enter = True
        input_value = entry.get().strip()
        if title == "新建名称" and not input_value == "未命名":
            func = option["callback"]
            func(option["setting_info"], input_value)
        root.destroy()
        return event

    def on_key_press(event):
        if event.keysym == "space":
            return "break"

    def on_focusout(event):
        """当输入框失去焦点时，直接退出"""
        if not click_enter:
            root.destroy()
        return event

    # 获取屏幕尺寸以计算布局参数，使窗口居中
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    size = (300, 60)
    x = int((screen_width - size[0]) / 2)
    y = int((screen_height - size[1]) / 2) - 60
    # 禁用窗口最大化按钮
    root.resizable(False, False)

    # 设置窗口初始位置在屏幕居中
    root.geometry(f'{size[0]}x{size[1]}+{x}+{y}')

    # 设置窗口保持在最前端
    root.attributes('-topmost', True)
    # 创建字体对象并设置字体大小
    custom_font = font.Font(family = "Microsoft YaHei", size = 20)

    # 创建一个输入框
    entry = tk.Entry(root, width=40, font = custom_font)
    entry.pack(padx=10, pady=10)
    entry.config(fg = 'gray')


    # 绑定事件处理函数
    entry.bind('<Return>', on_enter)  # 绑定Enter键
    entry.bind('<Escape>', on_esc)    # 绑定Esc键
    # 绑定按键事件
    entry.bind("<KeyPress>", on_key_press)
    # 焦点丢失事件
    entry.bind('<FocusOut>', on_focusout)
    entry.focus_set()

    # 运行主循环
    root.mainloop()
    return

# 使用线程管理，防止游戏主线程阻塞
def create_input_box(title: str, **option):
    thread = threading.Thread(target=__create_input_box,args = (title,option))
    # # 设为守护线程
    thread.daemon = True
    thread.start()
    return

# 一个自定义消息窗口
def message_box(title: str, content: str):
    # 创建一个自定义的消息框窗口
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    # 设置窗口保持在最前端
    root.attributes('-topmost', True)
    boolean = messagebox.askokcancel(title, content)
    root.destroy()
    # 运行主循环
    return boolean

