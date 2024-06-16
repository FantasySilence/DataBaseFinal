/* 3.1 */
create proc industrial_structure @Area nvarchar(50),
                                @Start_time nvarchar(50),
                                @End_time nvarchar(50)
as
    /* 查询分析指定时间周期一个经济区域的第一、二、三产业的产值占比分布及其变化 */
    if @Area in (select EconomicArea
                 from EconomicRegion)
        begin
            select Time,
                   sum(FirstIndustry_r) / (sum(FirstIndustry_r) + sum(SecondIndustry_r) + sum(ThirdIndustry_r))  第一产业占比,
                   sum(SecondIndustry_r) / (sum(FirstIndustry_r) + sum(SecondIndustry_r) + sum(ThirdIndustry_r)) 第二产业占比,
                   sum(ThirdIndustry_r) / (sum(FirstIndustry_r) + sum(SecondIndustry_r) + sum(ThirdIndustry_r))  第三产业占比
            from EconomicRegion_view
            where EconomicArea = @Area
              and Time between @Start_time and @End_time
            group by Time
        end
    /* 查询分析指定时间周期一个省的第一、二、三产业的产值占比分布及其变化 */
    if @Area in (select Province
                 from ProvincialInfo)
        begin
            select Time,
                   FirstIndustry / (FirstIndustry + SecondIndustry + ThirdIndustry)  第一产业占比,
                   SecondIndustry / (FirstIndustry + SecondIndustry + ThirdIndustry) 第二产业占比,
                   ThirdIndustry / (FirstIndustry + SecondIndustry + ThirdIndustry)  第三产业占比
            from ProvincialInfo
            where Province = @Area
              and Time between @Start_time and @End_time
        end
    /* 查询分析指定时间周期一个直辖市的第一、二、三产业的产值占比分布及其变化 */
    if @Area in (select City
                 from MunicipalityInfo)
        begin
            select Time,
                   FirstIndustry / (FirstIndustry + SecondIndustry + ThirdIndustry)  第一产业占比,
                   SecondIndustry / (FirstIndustry + SecondIndustry + ThirdIndustry) 第二产业占比,
                   ThirdIndustry / (FirstIndustry + SecondIndustry + ThirdIndustry)  第三产业占比
            from MunicipalityInfo
            where City = @Area
              and Time between @Start_time and @End_time
        end
    /* 查询分析指定时间周期一个省会城市的第一、二、三产业的产值占比分布及其变化 */
    if @Area in (select Capital
                 from ProvincialCapitalInfo)
        begin
            select Time,
                   FirstIndustry / (FirstIndustry + SecondIndustry + ThirdIndustry)  第一产业占比,
                   SecondIndustry / (FirstIndustry + SecondIndustry + ThirdIndustry) 第二产业占比,
                   ThirdIndustry / (FirstIndustry + SecondIndustry + ThirdIndustry)  第三产业占比
            from ProvincialCapitalInfo
            where Capital = @Area
              and Time between @Start_time and @End_time
        end
go

/* 3.2 */
create proc industrial_structure_compare @Area nvarchar(50),
                                         @Start_time nvarchar(50),
                                         @End_time nvarchar(50)
as
    if @Area = 'Area'
        begin
            select EconomicArea,
                   Time,
                   sum(FirstIndustry_r) /
                   (sum(FirstIndustry_r) + sum(SecondIndustry_r) + sum(ThirdIndustry_r)) 第一产业占比,
                   sum(SecondIndustry_r) /
                   (sum(FirstIndustry_r) + sum(SecondIndustry_r) + sum(ThirdIndustry_r)) 第二产业占比,
                   sum(ThirdIndustry_r) /
                   (sum(FirstIndustry_r) + sum(SecondIndustry_r) + sum(ThirdIndustry_r)) 第三产业占比
            from EconomicRegion_view
            where Time between @Start_time and @End_time
            group by Time, EconomicArea
        end
    if @Area = 'Province'
        begin
            select Province,
                   Time,
                   FirstIndustry / (FirstIndustry + SecondIndustry + ThirdIndustry)  第一产业占比,
                   SecondIndustry / (FirstIndustry + SecondIndustry + ThirdIndustry) 第二产业占比,
                   ThirdIndustry / (FirstIndustry + SecondIndustry + ThirdIndustry)  第三产业占比
            from ProvincialInfo
            where Time between @Start_time and @End_time

            union all

            select City,
                   Time,
                   FirstIndustry / (FirstIndustry + SecondIndustry + ThirdIndustry)  第一产业占比,
                   SecondIndustry / (FirstIndustry + SecondIndustry + ThirdIndustry) 第二产业占比,
                   ThirdIndustry / (FirstIndustry + SecondIndustry + ThirdIndustry)  第三产业占比
            from MunicipalityInfo
            where Time between @Start_time and @End_time
        end
go

/* 3.3 */
create proc industry_mode
as
DECLARE
    @TotalProvinces INT = (SELECT COUNT(DISTINCT Province)
                           FROM ProvincialInfo);

WITH PrePandemic AS (SELECT Province,
                            COUNT(*) AS CountNon321
                     FROM ProvincialInfo
                     WHERE Time = '2019'
                       AND NOT (FirstIndustry < SecondIndustry AND SecondIndustry < ThirdIndustry)
                     GROUP BY Province),
     PostPandemic AS (SELECT Province,
                             COUNT(*) AS CountNon321
                      FROM ProvincialInfo
                      WHERE Time = '2020'
                        AND NOT (FirstIndustry < SecondIndustry AND SecondIndustry < ThirdIndustry)
                      GROUP BY Province)

SELECT TimeFrame            = CASE
                                  WHEN p.Province IS NOT NULL THEN 'Before'
                                  WHEN pp.Province IS NOT NULL THEN 'After'
                                  ELSE NULL
                                  END,
                              p.Province  AS ProvinceBefore,
                              pp.Province AS ProvinceAfter,
       PreCountNon321       = CASE WHEN p.Province IS NOT NULL THEN p.CountNon321 ELSE NULL END,
       PostCountNon321      = CASE WHEN pp.Province IS NOT NULL THEN pp.CountNon321 ELSE NULL END,
       PrePercentageNon321  = CASE
                                  WHEN p.Province IS NOT NULL THEN CAST(p.CountNon321 AS FLOAT) / @TotalProvinces * 100
                                  ELSE NULL END,
       PostPercentageNon321 = CASE
                                  WHEN pp.Province IS NOT NULL
                                      THEN CAST(pp.CountNon321 AS FLOAT) / @TotalProvinces * 100
                                  ELSE NULL END
FROM PrePandemic p
         FULL OUTER JOIN
     PostPandemic pp ON p.Province = pp.Province
ORDER BY CASE
             WHEN p.Province IS NOT NULL THEN 1
             WHEN pp.Province IS NOT NULL THEN 2
             END,
         p.Province,
         pp.Province
go

/* 3.4 */
create procedure FindSimilarProvince
as
begin
    set nocount on;
    -- 第一步：计算湖北省每年的第二、三产业同比增长值的比值
    declare @HubeiRatios table
                         (
                             Time  int,
                             Ratio decimal(10, 2)
                         )
    insert into @HubeiRatios
    select Time, ISNULL(SecondIndustry / NULLIF(ThirdIndustry, 0), 0) as Ratio
    from ProvincialInfo
    where Province = N'湖北'
      and Time between 2020 and 2022

    -- 第二步：计算所有省份每年的第二、三产业同比增长值的比值
    declare @AllProvinceRatios table
                               (
                                   Province nvarchar(50),
                                   Time     int,
                                   Ratio    decimal(10, 2)
                               )
    insert into @AllProvinceRatios
    select Province, Time, ISNULL(SecondIndustry / NULLIF(ThirdIndustry, 0), 0) as Ratio
    from ProvincialInfo
    where Time between 2020 and 2022

    -- 第三步：计算每个省份与湖北省的相似度（这里使用简单的差值平方和）
    declare @Similarities table
                          (
                              Province   nvarchar(50),
                              Similarity decimal(10, 2)
                          );
    with CTE_Differences as (select a.Province,
                                    SUM(POWER(ISNULL(a.Ratio, 0) - ISNULL(h.Ratio, 0), 2)) AS DifferenceSum
                             from @AllProvinceRatios a
                                      inner join
                                  @HubeiRatios h on a.Time = h.Time
                             where a.Province <> N'湖北' -- 排除湖北省本身
                             group by a.Province)
    insert
    into @Similarities
    select Province, DifferenceSum as Similarity
    from CTE_Differences

    -- 第四步：按相似度排序，并取出最相似的三个省份
    select  Province,
                 Similarity
    from
        @Similarities
    order by Similarity
end
go
