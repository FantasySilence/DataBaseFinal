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
from src.common.infoTool.const import SQL_COMMAND
from src.ui.frame_interaction.commandexec import ExecuteSQLCommand


class ShowResultFrame(ttk.Frame):

    """
    查询结果展示页面
    """

    def __init__(self, master=None, **kw) -> None:
        
        # ------ 创建查询结果展示页面的根容器 ------ #
        super().__init__(master, **kw)
        self.pack_propagate(False)

        # ------ 创建查询结果显示的根容器 ------ #
        self.query_frame = ttk.Frame(self, width=750, height=750)
        self.query_frame.pack_propagate(False)
        self.query_frame.pack(pady=(10, 0), expand=True)

        # ------ 创建时间长度输入框的根容器 ------ #
        self.time_frame = ttk.Frame(self, width=750, height=40)
        self.time_frame.pack_propagate(False)
        self.time_frame.pack(pady=(0, 0), expand=True)

        self.scrollbar = None
        # 存储通信内容
        self.item_order = None
        self.temp = None

        self.start_time = ttk.StringVar(value="年份")
        self.end_time = ttk.StringVar(value="年份")
        self.area = ttk.StringVar(value="区域")

        self.create_page()

    
    def create_page(self) -> None:

        """
        创建页面
        """

        # ------ 创建显示查询结果的树状菜单 ------ #
        self.tree_view = ttk.Treeview(self.query_frame, height=10)
        self.tree_view.pack(fill=BOTH, expand=YES, side=LEFT)

        # ------ 插入数据 ------ #

        # ------ 数据量可能较大，设置一个滚动条 ------ #
        if self.scrollbar:
            pass
        else:
            self.scrollbar = ttk.Scrollbar(
                self.tree_view, orient="vertical", command=self.tree_view.yview
            )
            self.scrollbar.pack(side='right', fill='y')
            self.tree_view.configure(yscrollcommand=self.scrollbar.set)

        # ------ 创建三个输入框，用于填写查询区域与时间段 ------ #
        start_time_label = ttk.Label(self.time_frame, text="开始时间：", width=10)
        start_time_label.pack(side=LEFT, padx=(5, 0))
        start_time_entry = ttk.Entry(
            self.time_frame, textvariable=self.start_time, width=10
        )
        start_time_entry.pack(side=LEFT, padx=(0, 5))
        end_time_label = ttk.Label(self.time_frame, text="结束时间：", width=10)
        end_time_label.pack(side=LEFT, padx=(5, 0))
        end_time_entry = ttk.Entry(
            self.time_frame, textvariable=self.end_time, width=10
        )
        end_time_entry.pack(side=LEFT, padx=(0, 5))
        area_label = ttk.Label(self.time_frame, text="查询区域：", width=10)
        area_label.pack(side=LEFT, padx=(5, 0))
        area_entry = ttk.Entry(self.time_frame, textvariable=self.area, width=10)
        area_entry.pack(side=LEFT, padx=(0, 5))

        query_button = ttk.Button(
            self.time_frame, text="查询", command=self.query
        )
        query_button.pack(side=LEFT, padx=(5, 0))


    def load_res(self, item_order: str) -> None:

        """
        通信函数，返回选择的行
        """

        self.item_order = item_order


    def query(self):

        """
        查询
        """

        if self.item_order is not None:

            # ------ 清除Treeview中的旧数据 ------ #
            self.tree_view.delete(*self.tree_view.get_children())
            self.tree_view["columns"] = ()
            self.tree_view["show"] = ""

            # ------ 重新插入新的数据 ------ #
            self.tree_view["columns"] = tuple(SQL_COMMAND[self.item_order][1])
            self.tree_view["show"] = "headings"
            for column in self.tree_view["columns"]:
                self.tree_view.heading(column, text=column)
                self.tree_view.column(
                    column, width=int(750 / len(self.tree_view["columns"])), anchor=CENTER
                )
            sql_command = SQL_COMMAND[self.item_order][0]
            if self.area.get() == "区域" or self.area.get() == "":
                sql_command += ""
            else: 
                sql_command += "@Area=%s ," % self.area.get()

            if self.start_time.get() == "年份" or self.start_time.get() == "":
                sql_command += ""
            else:
                sql_command += "@Start_time=%s ," % self.start_time.get()

            if self.end_time.get() == "年份" or self.start_time.get() == "":
                sql_command += ""
            else:
                sql_command += "@End_time=%s" % self.end_time.get()

            print(sql_command)
            data = ExecuteSQLCommand.executes(sql_command)
            for i in range(len(data)):
                values = list(data[i])
                self.tree_view.insert("", "end", values=values)
            
            # ------ 清除输入框 ------ #
            self.area.set("")
            self.start_time.set("")
            self.end_time.set("")
        