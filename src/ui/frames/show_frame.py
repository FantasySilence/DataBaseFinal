# =================================== #
# @Author: Fantasy_Silence            #
# @Time: 2024-06-08                   #
# @IDE: Visual Studio Code & PyCharm  #
# @Python: 3.9.7                      #
# =================================== #
# @Description: 查询结果展示页面        #
# =================================== #
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class ShowResultFrame(ttk.Frame):

    """
    查询结果展示页面
    """

    def __init__(self, master=None, **kw) -> None:
        
        # ------ 创建查询结果展示页面的根容器 ------ #
        super().__init__(master, **kw)
        self.pack(fill=BOTH, expand=YES)
        self.pack_propagate(False)
    
    
    def create_page(self) -> None:

        """
        创建页面
        """

        pass
