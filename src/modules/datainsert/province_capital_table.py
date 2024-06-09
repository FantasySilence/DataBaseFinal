# =================================== #
# @Author: Fantasy_Silence            #
# @Time: 2024-06-04                   #
# @IDE: Visual Studio Code & PyCharm  #
# @Python: 3.9.7                      #
# =================================== #
# @Description: 省会城市设置表的数据插入#
# =================================== #
import pymssql
from src.common.infoTool.const import PROVINCE_CAPITAL_TABLE_NAME


class InsertIntoProvincialCapital:

    """
    向省会城市设置表中插入数据，便于数据库的快速搭建
    """

    @staticmethod
    def insert(
        province_capital: dict=None, database: str=None, *args, **kwargs
    ) -> None:
        
        # ------ 连接数据库 ------ #
        if database is None:
            # 默认情况下连接本地的数据库DataBaseFinal
            try:
                connection = pymssql.connect(
                    server='localhost', database='DataBaseFinal', autocommit=True
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
        if province_capital is None:
            # 默认插入全部的省会城市设置，不包含直辖市
            province_capital = PROVINCE_CAPITAL_TABLE_NAME
        for province, capital in province_capital.items():
            with connection.cursor() as cursor:
                # 尝试插入数据
                try:
                    cursor.execute(
                        f"INSERT INTO ProvincialCapital (Province, Capital) \
                        VALUES (N'{province}', N'{capital}')"
                    )
                # 如果数据已经插入就跳过
                except Exception:
                    print(f"({province}, {capital})已经添加过了，跳过...")
