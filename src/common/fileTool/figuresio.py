# ==================================================== #
# @Author: Fantasy_Silence                             #
# @Time: 2024-06-04                                    #
# @IDE: Visual Studio Code & PyCharm                   #
# @Python: 3.9.7                                       #
# ==================================================== #
# @Description: 图片文件IO类，便于图片的读取于储存        #
# ==================================================== #
import os


class FiguresIO:

    """
    图片文件IO类，便于图片的读取于储存
    """

    @staticmethod
    def loadFigPath(figname: str=None) -> str:

        """
        加载图片读取(保存)路径
        """

        common_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        src_path = os.path.dirname(common_path)
        ROOTPATH = os.path.dirname(src_path)
        resources_path = os.path.join(ROOTPATH, "resources")
        image_path = os.path.join(resources_path, "images")

        # ------ 不传入文件名默认返回存储文件的文件夹 ------ #
        if figname is None:
            return image_path
        else:
            return os.path.join(image_path, figname)
