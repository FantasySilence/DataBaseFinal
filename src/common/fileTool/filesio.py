# =========================================================== #
# @Author: Fantasy_Silence                                    #
# @Time: 2024-06-04                                           #
# @IDE: Visual Studio Code & PyCharm                          #
# @Python: 3.9.7                                              #
# =========================================================== #
# @Description: 文件IO流类，便于数据的读取以及SQL命令的加载      #
# =========================================================== #
import os


class FilesIO:

    """
    文件IO流类，便于数据的读取以及SQL命令的加载
    """

    @staticmethod
    def getDataSet(filename: str=None) -> str:

        """
        获取原始数据集路径，便于读取
        """

        common_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        src_path = os.path.dirname(common_path)
        ROOTPATH = os.path.dirname(src_path)
        resources_path = os.path.join(ROOTPATH, "resources")
        dataset_path = os.path.join(resources_path, "raw_data")
        
        # ------ 不传入文件名默认返回存储文件的文件夹 ------ #
        if filename is None:
            return dataset_path
        else:
            return os.path.join(dataset_path, filename)


    @staticmethod
    def loadSQLcommand(filename: str=None) -> str:

        """
        加载SQL命令
        """

        common_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        src_path = os.path.dirname(common_path)
        ROOTPATH = os.path.dirname(src_path)
        resources_path = os.path.join(ROOTPATH, "resources")
        sql_path = os.path.join(resources_path, "sql_command")

        # ------ 不传入文件名默认返回存储文件的文件夹 ------ #
        if filename is None:
            return sql_path
        else:
            return os.path.join(sql_path, filename)


    @staticmethod
    def loadUserInfo(filename: str=None) -> dict:

        """
        加载用户信息
        """

        common_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        src_path = os.path.dirname(common_path)
        ROOTPATH = os.path.dirname(src_path)
        resources_path = os.path.join(ROOTPATH, "resources")
        user_path = os.path.join(resources_path, "user_info")

        # ------ 不传入文件名默认返回存储文件的文件夹 ------ #
        if filename is None:
            return user_path
        else:
            return os.path.join(user_path, filename)
