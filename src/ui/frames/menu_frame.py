# =================================== #
# @Author: Fantasy_Silence            #
# @Time: 2024-06-08                   #
# @IDE: Visual Studio Code & PyCharm  #
# @Python: 3.9.7                      #
# =================================== #
# @Description: 树状菜单               #
# =================================== #
import re
import ttkbootstrap as ttk
from tkinter.font import Font
from ttkbootstrap.constants import *
from src.ui.frames.show_frame import ShowResultFrame


class TreeViewMenu(ttk.Frame):

    def __init__(self, master, res_page: ShowResultFrame, **kw) -> None:

        # ------ 创建树状菜单界面根容器 ------ #
        super().__init__(master, **kw)
        # 与结果显示界面建立通信
        self.res_page = res_page
        self.pack_propagate(False)
        self.create_page()


    def create_page(self) -> None:

        """
        创建页面
        """

        # ------ 标题栏 ------ #
        header_label = ttk.Label(
            self, text="经济数据查询", font=Font(family='宋体', size=20),
            bootstyle=(INVERSE, PRIMARY), anchor=CENTER
        )
        header_label.pack(pady=(10, 0), ipadx=390, ipady=20, fill=X, expand=True)

        # ------ 创建菜单 ------ #
        font = Font(family='宋体', size=12)
        ttk.Style().configure('Treeview', font=font, rowheight=30)
        self.tree_view = ttk.Treeview(
            self, show=TREE, height=10, style="Treeview",
        )
        self.tree_view.pack(
            pady=(0, 0), ipadx=390, ipady=760, fill=X, expand=True
        )
        
        # ------ 菜单内容 ------ #
        # 第一节
        self.tree_view.insert('', "end", '1', text='1.固定资产投资及社会消费品零售总额')
        self.tree_view.insert('1', "end", '1.1', text='1.1.固定资产总投资规模等')
        self.tree_view.insert('1', "end", '1.2', text='1.2.固定资产投资的差异')
        self.tree_view.insert('1', "end", '1.4', text='1.4.社会消费品零售总额增长趋势')
        # 第二节
        self.tree_view.insert('', "end", '2', text='2.全国生产总值增长趋势及区域差异')
        self.tree_view.insert('2', "end", '2.1', text='2.1.生产总值变化趋势分析')
        self.tree_view.insert('2', "end", '2.2', text='2.2.人均GDP差异分析')
        self.tree_view.insert('2', "end", '2.3', text='2.3.GDP变化差异')
        self.tree_view.insert('2', "end", '2.4', text='2.4.GDP增长趋势分析')
        # 第三节
        self.tree_view.insert('', "end", '3', text='3.全国产业结构变化及区域差异')
        self.tree_view.insert('3', "end", '3.1', text='3.1.产业产值占比分布与变化')
        self.tree_view.insert('3', "end", '3.2', text='3.2.产业产值占比')
        self.tree_view.insert('3', "end", '3.3', text='3.3.产业模式分析')
        self.tree_view.insert('3', "end", '3.4', text='3.4.产业相似度分析')
        # 第四节
        self.tree_view.insert('', "end", '4', text='4.居民收入变化及区域差异')
        self.tree_view.insert('4', "end", '4.1', text='4.1.各区域各项收入占比')
        self.tree_view.insert('4', "end", '4.2', text='4.2.区域人口特征')
        self.tree_view.insert('4', "end", '4.3', text='4.3.区域居民收入差异')
        self.tree_view.insert('4', "end", '4.4', text='4.4.居民收入环比增长趋势分析')
        self.tree_view.insert('4', "end", '4.5', text='4.5.居民收入同比增长趋势分析')

        # ------ 绑定功能 ------ #
        self.tree_view.bind('<<TreeviewSelect>>', self.on_select)


    def on_select(self, event):
        
        """
        选中某一个选项时进行相应的操作
        """

        selected_items = self.tree_view.selection()
        for item in selected_items:
            if not self.tree_view.get_children(item):  # 如果是叶子节点
                text = self.tree_view.item(item, 'text')
                item_order = re.findall(r'\d+\.\d+', text)[0]
                self.res_page.load_res(item_order)
    