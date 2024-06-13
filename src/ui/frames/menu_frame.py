# =================================== #
# @Author: Fantasy_Silence            #
# @Time: 2024-06-08                   #
# @IDE: Visual Studio Code & PyCharm  #
# @Python: 3.9.7                      #
# =================================== #
# @Description: 树状菜单               #
# =================================== #
import ttkbootstrap as ttk
from tkinter.font import Font
from ttkbootstrap.constants import *


class TreeViewMenu(ttk.Frame):

    def __init__(self, master=None, **kw) -> None:

        # ------ 创建树状菜单界面根容器 ------ #
        super().__init__(master, **kw)
        self.pack_propagate(False)
        self.pack(fill=BOTH, expand=YES)
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
        tree_view = ttk.Treeview(
            self, show=TREE, height=10, style="Treeview",
        )
        tree_view.pack(pady=(0, 0), ipadx=390, ipady=760, fill=X, expand=True)
        
        # ------ 菜单内容 ------ #
        # 第一节
        tree_view.insert('', "end", '1', text='1.固定资产投资及社会消费品零售总额')
        tree_view.insert('1', "end", '1.1', text='1.1.固定资产总投资规模等')
        tree_view.insert('1', "end", '1.2', text='1.2.固定资产投资的差异')
        tree_view.insert('1', "end", '1.3', text='1.3.社会消费品零售总额差异')
        tree_view.insert('1', "end", '1.4', text='1.4.社会消费品零售总额增长趋势')
        tree_view.insert('1', "end", '1.5', text='1.5.社会消费品零售总额增长趋势分')
        # 第二节
        tree_view.insert('', "end", '2', text='2.全国生产总值增长趋势及区域差异')
        tree_view.insert('2', "end", '2.1', text='2.1.生产总值变化趋势分析')
        tree_view.insert('2', "end", '2.2', text='2.2.人均GDP差异分析')
        tree_view.insert('2', "end", '2.3', text='2.3.GDP变化差异')
        tree_view.insert('2', "end", '2.4', text='2.4.GDP增长趋势分析')
        # 第三节
        tree_view.insert('', "end", '3', text='3.全国产业结构变化及区域差异')
        tree_view.insert('3', "end", '3.1', text='3.1.产业产值占比分布与变化')
        tree_view.insert('3', "end", '3.2', text='3.2.产业产值占比')
        tree_view.insert('3', "end", '3.3', text='3.3.产业模式分析')
        tree_view.insert('3', "end", '3.4', text='3.4.产业相似度分析')
        # 第四节
        tree_view.insert('', "end", '4', text='4.居民收入变化及区域差异')
        tree_view.insert('4', "end", '4.1', text='4.1.各区域各项收入占比')
        tree_view.insert('4', "end", '4.2', text='4.2.区域人口特征')
        tree_view.insert('4', "end", '4.3', text='4.3.区域居民收入差异')
        tree_view.insert('4', "end", '4.4', text='4.4.居民收入环比增长趋势分析')
        tree_view.insert('4', "end", '4.5', text='4.5.居民收入同比增长趋势分析')
        # 设置界面
        tree_view.insert('', "end", '5', text='5.设置')

        # ------ 绑定功能 ------ #
        tree_view.bind('<<TreeviewSelect>>', lambda event: print(event))
        