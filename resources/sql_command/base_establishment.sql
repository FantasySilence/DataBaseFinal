/*
 * 数据库创建与分表
 */

/* 省会城市设置（省或自治区名称，省会城市名称）不含直辖市 */
create table ProvincialCapital
(
    Province nvarchar(50) not null,
    Capital  nvarchar(50) not null,
    primary key (Province)
)

/* 经济区域划分（省级行政区名称，所属经济区域名称） */
/*
 区域：
 东北地区：辽宁省、吉林省、黑龙江省
 东部地区：北京市、天津市、河北省、上海市、江苏省、浙江省、
          福建省、山东省、广东省、海南省
 中部地区：山西省、安徽省、江西省、河南省、湖北省、湖南省
 西部地区：内蒙古自治区、广西壮族自治区、重庆市、四川省、
          贵州省、云南省、西藏自治区、陕西省、甘肃省、青海省、
          宁夏回族自治区、新疆维吾尔自治区
 */
create table EconomicRegion
(
    Province     nvarchar(50) not null,
    EconomicArea nvarchar(50) not null,
    primary key (Province)
)

/* 直辖市情况（直辖市名称，所处时间，区域面积，固定资产投资总额，……） */
create table MunicipalityInfo
(
    City              nvarchar(50) not null,
    Time              nvarchar(50) not null,
    Area              float,
    GDP               float,
    GDPperPerson      float,
    FirstIndustry     float,
    SecondIndustry    float,
    ThirdIndustry     float,
    PeopleIncome      float,
    SRG               float,
    FixedAssets       float,
    StateEconomy      float,
    CollectiveEconomy float,
    PrivateEconomy    float,
    StockEconomy      float,
    primary key (City, Time)
)

/* 省或自治区情况（省或自治区名称，所处时间，区域面积，固定资产投资总额，……） */
create table ProvincialInfo
(
    Province          nvarchar(50) not null,
    Time              nvarchar(50) not null,
    Area              float,
    GDP               float,
    GDPperPerson      float,
    FirstIndustry     float,
    SecondIndustry    float,
    ThirdIndustry     float,
    PeopleIncome      float,
    SRG               float,
    FixedAssets       float,
    StateEconomy      float,
    CollectiveEconomy float,
    PrivateEconomy    float,
    StockEconomy      float,
    primary key (Province, Time)
)

/* 省会城市情况（省或自治区名称，所处时间，区域面积，固定资产投资总额，……） */
create table ProvincialCapitalInfo
(
    Capital           nvarchar(50) not null,
    Time              nvarchar(50) not null,
    Area              float,
    GDP               float,
    GDPperPerson      float,
    FirstIndustry     float,
    SecondIndustry    float,
    ThirdIndustry     float,
    PeopleIncome      float,
    SRG               float,
    FixedAssets       float,
    StateEconomy      float,
    CollectiveEconomy float,
    PrivateEconomy    float,
    StockEconomy      float,
    primary key (Capital, Time)
)
