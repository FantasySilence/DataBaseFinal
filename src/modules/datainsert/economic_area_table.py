# =================================== #
# @Author: Fantasy_Silence            #
# @Time: 2024-06-04                   #
# @IDE: Visual Studio Code & PyCharm  #
# @Python: 3.9.7                      #
# =================================== #
# @Description: 经济区域表的数据插入    #
# =================================== #
import pymssql
from src.common.infoTool.const import ECONOMIC_REGION_TABLE_NAME


class InsertIntoEconomicRegion:

    """
    向经济区域表中插入数据，便于数据库的快速搭建
    """

    @staticmethod
    def insert(
        region_info: dict=None, database: str=None, *args, **kwargs
    ) -> None:
        
        # ------ 连接数据库 ------ #
        if database is None:
            # 默认情况下连接本地的数据库DataBaseFinal
            try:
                connection = pymssql.connect(
                    server='localhost', database='DataBaseFinal',autocommit=True
                )
            except:
                print("连接数据库失败，请检查数据库连接信息...")
        else:
            try:
                connection = pymssql.connect(
                    database=database, autocommit=True, *args, **kwargs
                )
            except:
                print("连接数据库失败，请检查数据库连接信息...")
        
        # ------ 插入数据 ------ #
        if region_info is None:
            # 默认插入全部的经济区域设置
            region_info = ECONOMIC_REGION_TABLE_NAME
        for region, province_list in region_info.items():
            for province in province_list:
                with connection.cursor() as cursor:
                    # 尝试插入数据
                    try:
                        cursor.execute(
                            f"INSERT INTO EconomicRegion (Province, EconomicArea) \
                            VALUES (N'{province}', N'{region}')"
                        )
                    # 如果数据已经插入就跳过
                    except Exception:
                        print(f"({province}, {region})已经添加过了，跳过...")
