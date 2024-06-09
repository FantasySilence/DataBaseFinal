# =================================== #
# @Author: Fantasy_Silence            #
# @Time: 2024-06-04                   #
# @IDE: Visual Studio Code & PyCharm  #
# @Python: 3.9.7                      #
# =================================== #
# @Description: 对原始数据进行处理      #
# =================================== #
import os
import numpy as np
import pandas as pd
from collections import defaultdict
from src.common.fileTool.filesio import FilesIO
from sklearn.base import BaseEstimator, TransformerMixin
from src.common.infoTool.const import PROVINCE_CAPITAL_TABLE_NAME


class PipelineForData(BaseEstimator, TransformerMixin):

    """
    对原始数据进行预处理，填补缺失值并整理，以便插入数据库
    """

    def __init__(self, is_save: bool=False) -> None:

        """
        传入两个原始数据集
        """

        self.is_save = is_save
    

    def fit(self, X, y=None):
        return self
    

    def transform(
            self, X_1: pd.DataFrame, X_2: pd.DataFrame, X_3: pd.DataFrame
    ) -> tuple[pd.DataFrame, pd.DataFrame]:

        """
        处理逻辑
        """

        # ------ 第一步，提取部分已经处理好的数据 ------ #
        # 根据索引直接获取
        idx = list(X_1.columns[1: 9])
        idx.extend(
            [
            "全体居民人均可支配收入(元)", "社会消费品零售总额(亿元)", 
            "固定资产投资(不含农户)增速(%)"
            ]
        )
        # 创建一个空矩阵用于存储数据
        res_1 = np.zeros((
            len(np.unique(X_1[idx].to_numpy()[:, 0])) * 6, 
            X_1[idx].to_numpy().shape[1]
        ), dtype=object)
        # 遍历空矩阵，将X_1中的数据填入(2017-2022年的数据)
        for i in range(res_1.shape[0]):
            try:
                res_1[i * 6: (i + 1) * 6, :] = X_1[idx].to_numpy()[
                    17 + 23 * i: 23 * (i + 1), :
                ]
            except:
                pass
        # 以DataFrame形式存储备用
        res_df_1 = pd.DataFrame(res_1, columns=idx)

        # ------ 第二步，有些指标需要额外计算 ------ #
        # 从X_2中提取2017年各个省份的固定资产投资总额
        data_to_use = X_2.loc[:, "2017年": "2018年"].iloc[:, :-1]
        # 修改列名并更改数据类型
        data_to_use.columns = data_to_use.iloc[0, :]
        data_to_use = data_to_use.iloc[1:, :].astype(float)
        data_to_use.index = X_2.iloc[1:, 0]
        # 创建一个空矩阵用于存储数据
        res_2 = np.zeros((len(data_to_use) * 6, 4), dtype=object)
        # 将2017年各个省份的固定资产投资总额存入字典，键为省份
        city_2017 = data_to_use.iloc[:, 0].to_dict(defaultdict(list))
        for i in range(len(data_to_use)):
            # 遍历空矩阵，填入省份名称与年份
            res_2[i * 6: (i + 1) * 6, :2] = res_df_1.iloc[i * 6: (i + 1) * 6, :2]
            # 遍历空矩阵，填入固定资产投资增速
            res_2[i * 6: (i + 1) * 6, 2] = res_df_1.iloc[i * 6: (i + 1) * 6, -1]
            # 遍历空矩阵，填入2017年各个省份的固定资产投资总额
            res_2[i * 6, 3] = city_2017[res_2[i * 6, 0]]
            # 根据增速与2017年数据，计算其余年份的固定资产投资总额
            for j in range(1, 6):
                res_2[i * 6 + j, 3] = res_2[i * 6 + j - 1, 3] * (1 + res_2[i * 6 + j, 2] / 100)
        # 以DataFrame形式存储备用
        res_df_2 = pd.DataFrame(
            res_2, columns=[
                "省份", "year", "固定资产投资(不含农户)增速(%)", 
                "固定资产投资额(万元)"
            ]
        )

        # ------ 第三步，将数据合并为一张表 ------ #
        province_data = pd.merge(
            left=res_df_1, right=res_df_2, on=["省份", "year"]
        ).drop(columns=[
            "固定资产投资(不含农户)增速(%)_x", "固定资产投资(不含农户)增速(%)_y",
            "GDP增速(%)"
        ])

        # ------ 第四步，处理并获取省会城市数据 ------ #
        # 直接截取数据
        X_3 = pd.concat([
            X_3.iloc[:, :11].drop(columns="行政区划代码"), 
            X_3["社会消费品零售总额(万元)"]
        ], axis=1)
        columns = list(X_3.columns)
        # 修改列名，与省级数据保持一致
        columns[1], columns[0] = "省会城市", "year"
        X_3.columns = columns
        # 提取合并的键
        X_4 = province_data.iloc[:, :2]
        X_4.columns = ["省会城市", "year"]
        for i in range(len(X_4)):
            if X_4.iloc[i, 0] in PROVINCE_CAPITAL_TABLE_NAME.keys():
                X_4.iloc[i, 0] = PROVINCE_CAPITAL_TABLE_NAME[X_4.iloc[i, 0]]
        
        capital_data = pd.merge(left=X_4, right=X_3, on=["省会城市", "year"])
        capital_data.insert(2, "GDP(亿元)", capital_data["地区生产总值(万元)"] / 10000)
        capital_data = capital_data.drop(columns="地区生产总值(万元)")
        capital_data.insert(3, "人均GDP(元)", capital_data["人均地区生产总值(元)"])
        capital_data = capital_data.drop(columns="人均地区生产总值(元)")
        capital_data["社会消费品零售总额(亿元)"] = capital_data["社会消费品零售总额(万元)"] / 10000
        capital_data = capital_data.drop(columns="社会消费品零售总额(万元)")
        capital_data.drop(
            columns=[
                "第一产业增加值占GDP比重(%)", "第二产业增加值占GDP比重(%)",
                "第三产业增加值占GDP比重(%)",
            ], inplace=True
        )
        capital_data[
            ["第一产业增加值(万元)", "第二产业增加值(万元)", "第三产业增加值(万元)"]
        ] = capital_data[
            ["第一产业增加值(万元)", "第二产业增加值(万元)", "第三产业增加值(万元)"]
        ].apply(lambda x: x / 10000)
        capital_data.columns = [
            "省会城市", "year", "GDP(亿元)", "人均GDP(元)",
            "第一产业增加值(亿元)", "第二产业增加值(亿元)", "第三产业增加值(亿元)",
            "社会消费品零售总额(亿元)"
        ]

        # ------ 第四步，持久化储存 ------ #
        if self.is_save:
            # 创建存放数据的文件夹
            folder_name = "processed_data"
            data_folder = os.path.join(FilesIO.getDataSet(), folder_name)
            if not os.path.exists(data_folder):
                os.mkdir(data_folder)
            # 储存数据
            province_data.to_csv(
                os.path.join(data_folder, "province_data.csv"), index=False
            )
            capital_data.to_csv(
                os.path.join(data_folder, "capital_data.csv"), index=False
            )
        
        # ------ 返回结果 ------ #
        return province_data, capital_data
