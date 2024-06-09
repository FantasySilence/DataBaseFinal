# =============================================== #
# @Author: Fantasy_Silence                        #
# @Time: 2024-06-06                               #
# @IDE: Visual Studio Code & PyCharm              #
# @Python: 3.9.7                                  #
# =============================================== #
# @Description: 省或自治区直辖市情况表的数据插入     #
# =============================================== #
import pymssql
import pandas as pd
from src.common.infoTool.const import PROVINCE_AREA, DIRECT_CITY


class InsertIntoProvincialInfo:

    """
    向省或自治区情况表插入数据，便于数据库的快速搭建
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
            if row["省份"] not in DIRECT_CITY:
                command = f"""
                INSERT INTO ProvincialInfo
                (
                Province, Time, Area, GDP, GDPperPerson,
                FirstIndustry, SecondIndustry, ThirdIndustry,
                PeopleIncome, SRG, FixedAssets,
                StateEconomy, CollectiveEconomy, PrivateEconomy, StockEconomy
                )
                VALUES
                (
                N'{row["省份"]}', {row["year"]}, {PROVINCE_AREA[row["省份"]]}, 
                {row["GDP(亿元)"]}, {row["人均GDP(元)"]}, 
                {row["第一产业增加值(亿元)"]}, {row["第二产业增加值(亿元)"]}, 
                {row["第三产业增加值(亿元)"]}, {row["全体居民人均可支配收入(元)"]},
                {row["社会消费品零售总额(亿元)"]}, {row["固定资产投资额(万元)"]}, 
                null, null, null, null
                )
                """
                with connection.cursor() as cursor:
                    # 尝试插入数据
                    try:
                        cursor.execute(command)
                    # 如果数据已经插入就跳过
                    except Exception:
                       print(f'({row["省份"]}, {row["year"]})已经添加过了，跳过...')
            
            # 插入直辖市情况表
            else:
                command = f"""
                INSERT INTO MunicipalityInfo
                (
                City, Time, Area, GDP, GDPperPerson,
                FirstIndustry, SecondIndustry, ThirdIndustry,
                PeopleIncome, SRG, FixedAssets,
                StateEconomy, CollectiveEconomy, PrivateEconomy, StockEconomy
                )
                VALUES
                (
                N'{row["省份"]}', {row["year"]}, {PROVINCE_AREA[row["省份"]]}, 
                {row["GDP(亿元)"]}, {row["人均GDP(元)"]}, 
                {row["第一产业增加值(亿元)"]}, {row["第二产业增加值(亿元)"]}, 
                {row["第三产业增加值(亿元)"]}, {row["全体居民人均可支配收入(元)"]},
                {row["社会消费品零售总额(亿元)"]}, {row["固定资产投资额(万元)"]}, 
                null, null, null, null
                )
                """
                with connection.cursor() as cursor:
                    # 尝试插入数据
                    try:
                        cursor.execute(command)
                    # 如果数据已经插入就跳过
                    except Exception:
                       print(f'({row["省份"]}, {row["year"]})已经添加过了，跳过...')
                