# ================================================= #
# @Author: Fantasy_Silence                          #
# @Time: 2024-06-07                                 #
# @IDE: Visual Studio Code & PyCharm                #
# @Python: 3.9.7                                    #
# ================================================= #
# @Description: 如果数据库寄了,这个模块可以救你        #
# ================================================= #
import pymssql
import pandas as pd

from src.common.fileTool.filesio import FilesIO
from src.modules.datapreparation.pipelines import PipelineForData
from src.modules.datainsert.province_info import InsertIntoProvincialInfo
from src.modules.datainsert.economic_area_table import InsertIntoEconomicRegion
from src.modules.datainsert.province_capital_table import InsertIntoProvincialCapital
from src.modules.datainsert.provincial_capital_info import InsertIntoProvincialCapitalInfo


class QuickRepair:

    """
    数据库本体的快速恢复
    """

    @staticmethod
    def restore(server: str=None) -> None:

        # ------ 读取创建命令 ------ #
        with open(
            FilesIO.loadSQLcommand("base_establishment.sql"), encoding="utf-8"
        ) as f:
            sql = f.read()

        # ------ 连接数据库 ------ #
        try:
            if server is not None:
                connection = pymssql.connect(server=server, autocommit=True)
            else:
                connection = pymssql.connect(server='localhost', autocommit=True)
        except:
            print("连接数据库失败，请检查数据库连接信息...")

        # ------ 创建数据库以及数据表 ------ #
        with connection.cursor() as cursor:
            cursor.execute("DROP DATABASE IF EXISTS DataBaseFinal")
            cursor.execute("CREATE DATABASE DataBaseFinal")
            cursor.execute("USE DataBaseFinal")
            cursor.execute(sql)
        connection.close()

        # ------ 处理数据,等待插入 ------ #
        data_1 = pd.read_excel(
            FilesIO.getDataSet("2000-2022年全国、各省数据.xlsx"), 
            sheet_name="各省数据"
        )
        data_2 = pd.read_excel(
            FilesIO.getDataSet("不同类型固定资产投资.xlsx")
        )
        data_3 = pd.read_excel(
            FilesIO.getDataSet("中国城市数据库.xlsx"), sheet_name="线性插值"
        )
        _, _ = PipelineForData(is_save=True).transform(
            data_1, data_2, data_3
        )

        # ------ 插入数据 ------ #
        # 向经济区域表中插入数据
        InsertIntoEconomicRegion.insert()
        # 向省会城市表中插入数据
        InsertIntoProvincialCapital.insert()
        # 向省或自治区直辖市情况表中插入数据
        InsertIntoProvincialInfo.insert(
            pd.read_csv(FilesIO.getDataSet("processed_data/province_data.csv"))
        )
        # 向省会城市情况表中插入数据
        InsertIntoProvincialCapitalInfo.insert(
            pd.read_csv(FilesIO.getDataSet("processed_data/capital_data.csv"))
        )
