/* 1.1 */
create proc investmentscale @Area nvarchar(50),
                            @start_time nvarchar(50),
                            @end_time nvarchar(50)
as
    /* 经济区域一级 */
    if @Area in (select economicarea
                 from economicregion)
        begin
            select Time,
                   FixedAssets_r                               as totalfixedassets,
                   (StateEconomy_r / FixedAssets_r) * 100      as stateeconomypercentage,
                   (CollectiveEconomy_r / FixedAssets_r) * 100 as collectiveeconomypercentage,
                   (PrivateEconomy_r / FixedAssets_r) * 100    as privateeconomypercentage,
                   (StockEconomy_r / FixedAssets_r) * 100      as stockeconomypercentage
            from EconomicRegion_view
            where EconomicArea=@Area
              and Time between @start_time and @end_time
              and FixedAssets_r > 0
        end

    /* 省级 */
    if @Area in (select province
                 from provincialinfo)
        begin
            select Time,
                   FixedAssets                             as totalfixedassets,
                   (StateEconomy / FixedAssets) * 100      as stateeconomypercentage,
                   (CollectiveEconomy / FixedAssets) * 100 as collectiveeconomypercentage,
                   (PrivateEconomy / FixedAssets) * 100    as privateeconomypercentage,
                   (StockEconomy / FixedAssets) * 100      as stockeconomypercentage
            from provincialinfo
            where Province = @Area
              and time between @start_time and @end_time
              and FixedAssets > 0
        end

    /* 直辖市 */
    if @Area in (select City
                 from MunicipalityInfo)
        begin
            select Time,
                   FixedAssets                             as totalfixedassets,
                   (StateEconomy / FixedAssets) * 100      as stateeconomypercentage,
                   (CollectiveEconomy / FixedAssets) * 100 as collectiveeconomypercentage,
                   (PrivateEconomy / FixedAssets) * 100    as privateeconomypercentage,
                   (StockEconomy / FixedAssets) * 100      as stockeconomypercentage
            from MunicipalityInfo
            where City = @Area
              and time between @start_time and @end_time
              and FixedAssets > 0
        end
go

/* 1.2 */
create proc investmentdifference @Area nvarchar(50),
                                 @start_time nvarchar(50),
                                 @end_time nvarchar(50)
as
    if @Area = 'province'
        begin
            select Province,
               Time,
               FixedAssets
        from ProvincialInfo
        where time between @start_time and @end_time

        union all

        select City,
               Time,
               FixedAssets
        from MunicipalityInfo
        where time between @start_time and @end_time
        order by FixedAssets desc
        end
    if @Area = 'area'
        begin
            select EconomicArea,
                   Time,
                   FixedAssets_r
            from EconomicRegion_view
            where time between @start_time and @end_time
            order by FixedAssets_r desc
        end
go

/* 1.4 */
create proc SRGinPandemic
as
    with SRG_Changes as (
        -- 计算每个省份在连续三年的社会消费品零售总额增长率
        select
            p2020.Province,
            (p2020.SRG - p2019.SRG) / NULLIF(p2019.SRG, 0) as Growth2020,
            (p2021.SRG - p2020.SRG) / NULLIF(p2020.SRG, 0) as Growth2021,
            (p2022.SRG - p2021.SRG) / NULLIF(p2021.SRG, 0) as Growth2022
        from
            ProvincialInfo as p2020
            join ProvincialInfo as p2019 on p2020.Province = p2019.Province and p2019.Time = '2019'
            join ProvincialInfo as p2021 on p2020.Province = p2021.Province and p2021.Time = '2021'
            join ProvincialInfo as p2022 on p2020.Province = p2022.Province and p2022.Time = '2022'
        where
            p2020.Time = '2020'
    ),
    Filtered_Provinces as (
        -- 筛选出满足条件的省份
        select Province
        from SRG_Changes
        where Growth2020 < 0
          and Growth2021 > 0
          and Growth2022 < 0
    ),
    Total_Provinces as (
        -- 计算2020年所有省份的数量
        select COUNT(distinct Province) as TotalProvinceCount
        from ProvincialInfo
        where Time = '2020'
    )
    -- 最终查询，输出满足条件的省份及比例
    select
        fp.Province,
        (select count(*) from Filtered_Provinces) as AffectedProvincesCount,
        (select TotalProvinceCount from Total_Provinces) as TotalProvincesCount,
        cast((select count(*) from Filtered_Provinces) as float) /
        (select TotalProvinceCount from Total_Provinces) as Proportion
    from Filtered_Provinces fp;
go
