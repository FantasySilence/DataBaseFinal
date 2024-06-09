# =================================== #
# @Author: Fantasy_Silence            #
# @Time: 2024-06-08                   #
# @IDE: Visual Studio Code & PyCharm  #
# @Python: 3.9.7                      #
# =================================== #
# @Description: 登陆界面               #
# =================================== #
import json
import ttkbootstrap as ttk
from tkinter.font import Font
from tkinter import messagebox
from ttkbootstrap.constants import *
from src.common.fileTool.filesio import FilesIO


class LoginWindow(ttk.Frame):

    """
    登陆界面
    """
    
    def __init__(self, master=None, show_menu=None, **kw) -> None:

        # ------ 创建登陆界面的根容器 ------ #
        super().__init__(master, **kw)
        copyright_label = ttk.Label(
            self, 
            text="Powered by: Fantasy_Silence. All rights reserved", 
            font=Font(family='Times New Roman', size=10),
            anchor=CENTER, bootstyle=PRIMARY
        )
        more_detail_label = ttk.Label(
            self, 
            text="More detail: https://github.com/FantasySilence/DataBaseFinal",
            font=Font(family='Times New Roman', size=10),
            anchor=CENTER, bootstyle=PRIMARY
        )
        more_detail_label.pack(side=BOTTOM, pady=(0, 10))
        copyright_label.pack(side=BOTTOM, pady=(140, 3))
        self.pack(fill=BOTH, expand=YES)

        # ------ 登录页和信息页的通信 ------ #
        self.show_menu = show_menu

        # ------ 创建存放输入框的根容器 ------ #
        self.entry_frame = ttk.Frame(self, width=600, height=300)
        self.entry_frame.pack(padx=270, pady=(100, 10), side=TOP)
        self.entry_frame.pack_propagate(False)

        # ------ 创建存放按钮的根容器 ------ #
        self.button_frame = ttk.Frame(self, width=600, height=100)
        self.button_frame.pack(padx=270, pady=(0, 100), side=BOTTOM)
        self.button_frame.pack_propagate(False)
        
        self.create_page()
    

    def create_page(self):

        """
        创建页面
        """

        # ------ 标题栏 ------ #
        header_label = ttk.Label(
            self.entry_frame, text="欢迎使用xx数据库系统，请登录...", 
            font=Font(family='宋体', size=20), anchor=CENTER
        )
        header_label.pack(pady=(0, 0), ipadx=600, ipady=20)
    
        # ------ 输入用户名 ------ #
        user_label = ttk.Label(
            self.entry_frame, text="请输入您的用户名：", 
            font=Font(family='宋体', size=14),
            anchor=CENTER
        )
        user_label.pack(pady=(10, 0), ipadx=600, ipady=20)
        self.user_entry = ttk.Entry(
            self.entry_frame, bootstyle=PRIMARY, width=30
        )
        self.user_entry.pack(pady=(0, 0))

        # ------ 输入密码 ------ #
        password_label = ttk.Label(
            self.entry_frame, text="请输入您的密码：", 
            font=Font(family='宋体', size=14),
            anchor=CENTER
        )
        password_label.pack(pady=(0, 0), ipadx=600, ipady=20)
        self.password_entry = ttk.Entry(
            self.entry_frame, bootstyle=PRIMARY, width=30, show="*"
        )
        self.password_entry.pack(pady=(0, 10))

        # ------ 登录按钮 ------ #
        login_button = ttk.Button(
            self.button_frame, text="登陆", command=self.login,
            bootstyle=SUCCESS,
        )
        login_button.pack(
            padx=(30, 0), pady=10, ipadx=100, ipady=10, side=LEFT
        )

        # ------ 退出按钮 ------ #
        quit_button = ttk.Button(
            self.button_frame, text="退出", command=self.quit,
            bootstyle=DANGER,
        )
        quit_button.pack(
            padx=(0, 30), pady=10, ipadx=100, ipady=10, side=RIGHT
        )


    def login(self):

        """
        登陆
        """

        # ------ 读取用户信息 ------ #
        with open(FilesIO.loadUserInfo("user.json"), "r") as f:
            user_info = json.load(f)
        
        # ------ 进行账密验证 ------ #
        user_name = self.user_entry.get()
        password = self.password_entry.get()

        # 验证成功显示页面
        if user_name in user_info.keys() and password == user_info[user_name]:
            self.show_menu()
        # 验证失败，报错
        else:
            self.user_entry.delete(0, END)
            self.password_entry.delete(0, END)
            self.user_entry.focus()
            messagebox.showerror("错误", "用户名或密码错误！")
       