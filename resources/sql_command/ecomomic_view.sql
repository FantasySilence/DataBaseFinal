/* 经济区域情况（省级行政区名称，所处时间，区域面积，固定资产投资总额，……）视图 */
create view EconomicRegion_view as
select EconomicRegion.EconomicArea,
       ProvincialInfo.Time,
       sum(Area)              Area_r,
       sum(GDP)               GDP_r,
       sum(GDPperPerson)      GDPperPerson_r,
       sum(FirstIndustry)     FirstIndustry_r,
       sum(SecondIndustry)    SecondIndustry_r,
       sum(ThirdIndustry)     ThirdIndustry_r,
       sum(PeopleIncome)      PeopleIncome_r,
       sum(SRG)               SRG_r,
       sum(FixedAssets)       FixedAssets_r,
       sum(StateEconomy)      StateEconomy_r,
       sum(CollectiveEconomy) CollectiveEconomy_r,
       sum(PrivateEconomy)    PrivateEconomy_r,
       sum(StockEconomy)      StockEconomy_r
from ProvincialInfo
         join EconomicRegion
              on ProvincialInfo.Province = EconomicRegion.Province
group by ProvincialInfo.Time, EconomicRegion.EconomicArea
