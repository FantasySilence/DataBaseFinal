# =================================== #
# @Author: Fantasy_Silence            #
# @Time: 2024-06-06                   #
# @IDE: Visual Studio Code & PyCharm  #
# @Python: 3.9.7                      #
# =================================== #
# @Description: 省会城市情况表的数据插入#
# =================================== #
import pymssql
import pandas as pd
from src.common.infoTool.const import PROVINCE_CAPITAL_AREA, DIRECT_CITY


class InsertIntoProvincialCapitalInfo:

    """
    向省会城市设置表中插入数据，便于数据库的快速搭建
    """

    @staticmethod
    def insert(data: pd.DataFrame, database: str=None, *args, **kwargs)-> None:

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
        
        # ------ 根据原始数据处理后的结果向表中插入数据 ------ #
        for _, row in data.iterrows():
            # 插入省或自治区情况表
            if row["省会城市"] not in DIRECT_CITY:
                command = f"""
                INSERT INTO ProvincialCapitalInfo
                (
                Capital, Time, Area, GDP, GDPperPerson,
                FirstIndustry, SecondIndustry, ThirdIndustry,
                PeopleIncome, SRG, FixedAssets,
                StateEconomy, CollectiveEconomy, PrivateEconomy, StockEconomy
                )
                VALUES
                (
                N'{row["省会城市"]}', {row["year"]}, 
                {PROVINCE_CAPITAL_AREA[row["省会城市"]]}, {row["GDP(亿元)"]}, 
                {row["人均GDP(元)"]}, 
                {row["第一产业增加值(亿元)"]}, {row["第二产业增加值(亿元)"]}, 
                {row["第三产业增加值(亿元)"]}, null, {row["社会消费品零售总额(亿元)"]},
                null, null, null, null, null 
                )
                """
                with connection.cursor() as cursor:
                    # 尝试插入数据
                    try:
                        cursor.execute(command)
                    # 如果数据已经插入就跳过
                    except Exception as e:
                        print(e)
                        print(f'({row["省会城市"]}, {row["year"]})已经添加过了，跳过...')
