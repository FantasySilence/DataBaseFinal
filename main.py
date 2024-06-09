# =================================== #
# @Author: Fantasy_Silence            #
# @Time: 2024-06-04                   #
# @IDE: Visual Studio Code & PyCharm  #
# @Python: 3.9.7                      #
# =================================== #
# @Description: 这里是主程序入口       #
# =================================== #
# TODO: 目前需要做的任务
"""
1.建库分表(已完成)
2.插入数据，经济数据指标尚不明确，数据需要进行进一步处理(已完成)
3.编写查询逻辑，注意兼容UI界面交互
4.设计并实现UI界面(已完成)
5.相关工具类的编写，包括文件IO，绘图模块等
6.(暂定)部署服务器，并编写登录UI
"""
from src.modules.ui.mainwindow import MainFrame

MainFrame.show()
