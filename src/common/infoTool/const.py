# =================================== #
# @Author: Fantasy_Silence            #
# @Time: 2024-06-04                   #
# @IDE: Visual Studio Code & PyCharm  #
# @Python: 3.9.7                      #
# =================================== #
# @Description: 一些常量表             #
# =================================== #

# ------ 国家经济分区 ------ #
ECONOMIC_REGION_TABLE_NAME = {
    "东北地区": ["辽宁", "吉林", "黑龙江"],
    "中部地区": ["山西", "安徽", "江西", "河南", "湖北", "湖南"],
    "东部地区": [
        "北京", "天津", "河北", "上海", "江苏", "浙江", 
        "福建", "山东", "广东", "海南"
    ],
    "西部地区": [
        "内蒙古", "广西", "重庆", "四川",
        "贵州", "云南", "西藏", "陕西", "甘肃", "青海",
        "宁夏", "新疆"
    ],
}

# ------ 省会城市(不含直辖) ------ #
PROVINCE_CAPITAL_TABLE_NAME = {
    "安徽": "合肥", "江苏": "南京", "浙江": "杭州", 
    "江西": "南昌", "福建": "福州", "广东": "广州", 
    "湖南": "长沙", "湖北": "武汉", "山东": "济南", 
    "河南": "郑州", "河北": "石家庄", "山西": "太原", 
    "辽宁": "沈阳", "吉林": "长春", "黑龙江": "哈尔滨", 
    "贵州": "贵阳", "云南": "昆明", "陕西": "西安",
    "甘肃": "兰州", "青海": "西宁", "广西": "南宁",
    "西藏": "拉萨", "宁夏": "银川", "新疆": "乌鲁木齐",
    "内蒙古": "呼和浩特", "四川": "成都", "海南": "海口"
}

# ------ 省会城市行政区域面积 ------ #
PROVINCE_CAPITAL_AREA = {
    "合肥": 11445, "南京": 6587, "杭州": 16850, 
    "南昌": 7195, "福州": 11968, "广州": 7434, 
    "长沙": 11819, "武汉": 8569, "济南": 10244, 
    "郑州": 7567, "石家庄": 14464, "太原": 6988, 
    "沈阳": 12860, "长春": 24744, "哈尔滨": 53100, 
    "贵阳": 8034, "昆明": 21013, "西安": 10108,
    "兰州": 13100, "西宁": 7660, "南宁": 22100,
    "拉萨": 31662, "银川": 9025, "乌鲁木齐": 12800,
    "呼和浩特": 17200, "成都": 14335, "海口": 3127,
}

# ------ 各省，自治区，直辖市行政区域面积 ------ #
PROVINCE_AREA = {
    "安徽": 140100, "江苏": 107200, "浙江": 105500, 
    "江西": 166900, "福建": 124000, "广东": 179725, 
    "湖南": 211800, "湖北": 185900, "山东": 155800, 
    "河南": 167000, "河北": 188800, "山西": 156700, 
    "辽宁": 148000, "吉林": 187400, "黑龙江": 473000, 
    "贵州": 176167, "云南": 394100, "陕西": 205600,
    "甘肃": 425800, "青海": 722300, "广西": 237600,
    "西藏": 1228400, "宁夏": 66400, "新疆": 1664900,
    "内蒙古": 1183000, "四川": 486000, "海南": 35400,
    "北京": 16418, "天津": 11934, "上海": 6340, "重庆": 82370
}

# ------ 直辖市 ------ #
DIRECT_CITY = ["北京", "天津", "上海", "重庆"]
