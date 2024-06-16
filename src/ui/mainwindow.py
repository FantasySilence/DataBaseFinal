# =================================== #
# @Author: Fantasy_Silence            #
# @Time: 2024-06-08                   #
# @IDE: Visual Studio Code & PyCharm  #
# @Python: 3.9.7                      #
# =================================== #
# @Description: 主界面(所有控件的根容器)#
# =================================== #
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from src.ui.frames.menu_frame import TreeViewMenu
from src.ui.frames.login_frame import LoginWindow
from src.ui.frames.show_frame import ShowResultFrame


class MainFrame(ttk.Frame):
    
    """
    主界面
    """

    def __init__(self, master=None, **kw) -> None:
        
        # ------ 创建主窗口页面的根容器 ------ #
        super().__init__(master, **kw)
        self.pack(fill=BOTH, expand=YES)

        # ------ 创建登录界面的根容器 ------ #
        self.login_frame = ttk.Frame(self, width=1140, height=800)
        self.login_frame.pack(fill=BOTH, expand=YES)
        self.login_frame.pack_propagate(False)

        # ------ 创建主界面的根容器 ------ #
        self.mainframe = ttk.Frame(self, width=1140, height=800)
        self.mainframe.pack_propagate(False)
        
        self.create_page()

    
    def create_page(self) -> None:

        """
        创建登录页面
        """
        
        # ------ 登录界面 ------ #
        login_frame = LoginWindow(
            master=self.login_frame, 
            show_menu=self.show_main_page,
            width=1140, height=800
        )
        login_frame.grid(row=0, column=0, sticky=NS)
        

    
    def show_main_page(self) -> None:

        """
        显示主界面
        """

        self.login_frame.pack_forget()
        self.mainframe.pack(fill=BOTH, expand=YES)
        
        # ------ 展示界面 ------ #
        show_frame = ShowResultFrame(self.mainframe, width=750, height=800)
        show_frame.grid(row=0, column=1, sticky=NS)

        # ------ 树状菜单界面 ------ #
        menu_frame = TreeViewMenu(self.mainframe, show_frame, width=390, height=800)
        menu_frame.grid(row=0, column=0, sticky=NS)



    @staticmethod
    def _show() -> None:
        root = ttk.Window(
            title="数据库期末项目 v0.2", themename="minty", size=(1140, 800)
        )
        # root.resizable(False, False)
        MainFrame(root)
        root.mainloop()

    @classmethod
    def show(cls) -> None:
        MainFrame._show()

