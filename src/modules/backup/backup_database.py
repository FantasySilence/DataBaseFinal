# =================================== #
# @Author: Fantasy_Silence            #
# @Time: 2024-06-07                   #
# @IDE: Visual Studio Code & PyCharm  #
# @Python: 3.9.7                      #
# =================================== #
# @Description: 数据库的快速备份与回档  #
# =================================== #
import pymssql
import datetime
from src.common.fileTool.filesio import FilesIO


class QuickBackup:

    """
    数据库备份工具,用于创建备份与回档
    """

    @staticmethod
    def backup(server: str=None, *args, **kwargs):

        """
        备份
        """

        # ------ 连接数据库 ------ #
        if server is None:
            # 默认连接本地数据库
            try:
                connection = pymssql.connect(
                    server="localhost", autocommit=True, *args, **kwargs
                )
            except:
                print("连接失败")
        else:
            try:
                connection = pymssql.connect(
                    server, autocommit=True, *args, **kwargs
                )
            except:
                print("连接失败")

        # ------ 执行备份命令 ------ #
        cursor = connection.cursor()
        cursor.execute(f"EXEC back_up {FilesIO.save_backup(
            str(datetime.datetime.now()).split('.')[0].replace(':', '-')
        )}")
        connection.close()
    

    @staticmethod
    def restore(
        backup: str, log_path:str, data_path: str, 
        server: str=None, *args, **kwargs
    ):

        """
        回档
        """

        # ------ 连接数据库 ------ #
        if server is None:
            # 默认连接本地数据库
            try:
                connection = pymssql.connect(
                    server="localhost", autocommit=True, *args, **kwargs
                )
            except:
                print("连接失败")
        else:
            try:
                connection = pymssql.connect(
                    server, autocommit=True, *args, **kwargs
                )
            except:
                print("连接失败")

        # ------ 执行回档命令 ------ #
        cursor = connection.cursor()
        cursor.execute(f"EXEC restore_ {backup} {data_path} {log_path}")
        cursor.close()
