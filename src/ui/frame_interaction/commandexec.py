# =================================================== #
# @Author: Fantasy_Silence                            #
# @Time: 2024-06-16                                   #
# @IDE: Visual Studio Code & PyCharm                  #
# @Python: 3.9.7                                      #
# =================================================== #
# @Description: 这个模块用于执行相应的SQL命令            #
# =================================================== #
import pymssql
import numpy as np


class ExecuteSQLCommand:

    """
    执行SQL命令并返回结果
    """

    @staticmethod
    def executes(sql_command: str) -> np.ndarray:

        """
        执行命令
        """

        # ------ 连接到数据库 ------ #
        connection = pymssql.connect(
            server="localhost", database="DataBaseFinal", autocommit=True
        )

        # ------ 执行命令并存储 ------ #
        with connection.cursor() as cursor:
            cursor.execute(sql_command)
            result = cursor.fetchall()
            res = np.zeros((len(result), len(result[0])), dtype=object)
            for i in range(len(result)):
                res[i] = list(result[i])
        connection.close()

        # ------ 返回结果 ------ #
        res = np.array([
            [ExecuteSQLCommand.round_if_float(x, decimals=2) for x in row] 
            for row in res
        ], dtype=object)

        return res
    
    @staticmethod
    def round_if_float(x, decimals=2):
        if isinstance(x, float):
            return round(x, decimals)
        return x
