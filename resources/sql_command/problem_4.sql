/* 4.1 */
create proc income
as
    select
        Province,
        Time,
        FirstIndustry / GDP as FirstIndustryRatio,
        SecondIndustry / GDP as SecondIndustryRatio,
        ThirdIndustry / GDP as ThirdIndustryRatio
    from
        ProvincialInfo
    order by
        Province, Time;
go
    
/* 4.2 */
create proc income_compare @start_time nvarchar(50),
                           @end_time nvarchar(50)
as
WITH RankedProvinces AS (SELECT Province,
                                Area,
                                GDP,
                                GDPperPerson,
                                PeopleIncome,
                                GDP * 100000000/ (GDPperPerson * Area)              AS PopulationDensity,
                                RANK() OVER (ORDER BY PeopleIncome DESC) AS HighIncomeRank,
                                RANK() OVER (ORDER BY PeopleIncome) AS LowIncomeRank
                         FROM ProvincialInfo
                         WHERE Time between @start_time and @end_time)

SELECT Province,
       Area,
       GDP,
       GDPperPerson,
       PeopleIncome,
       PopulationDensity
FROM RankedProvinces
WHERE HighIncomeRank <= 3
   or LowIncomeRank <= 3
order by PeopleIncome Desc
go

/* 4.3 */
CREATE TABLE PeopleIncomeLevels
(
    Time          char(4), -- 假设年份为4位数
    LowThreshold  decimal(10, 2),
    HighThreshold decimal(10, 2)
);

insert into PeopleIncomeLevels (Time, LowThreshold, HighThreshold)
values ('2017', 20000.0, 30000.0), -- 假设2017年的低高阈值
       ('2018', 20000.0, 35000.0), -- 假设2018年的低高阈值
       ('2019', 20000.0, 35000.0), -- 假设2019年的低高阈值
       ('2020', 25000.0, 40000.0), -- 假设2020年的低高阈值
       ('2021', 30000.0, 40000.0), -- 假设2021年的低高阈值
       ('2022', 30000.0, 45000.0) -- 假设2022年的低高阈值
go

create procedure FindConsistentIncomeLevels @Area nvarchar(50) = N'高'
as
begin
    if @Area = N'高'
        begin
            -- 高收入省份列表
            with HighIncomeProvinces as (select p.Province
                                         from ProvincialInfo p
                                                  inner join
                                              PeopleIncomeLevels pil on p.Time = pil.Time
                                         where p.Time between '2017' and '2022'
                                           and p.PeopleIncome >= pil.HighThreshold
                                         group by p.Province
                                         having COUNT(distinct p.Time) = 6 -- 确保所有六年都在高收入范围内
            )
            select distinct Province
            from HighIncomeProvinces;
        end

    if @Area = N'低'
        begin
            -- 低收入省份列表
            with LowIncomeProvinces as (select p.Province
                                        from ProvincialInfo p
                                                 inner join
                                             PeopleIncomeLevels pil on p.Time = pil.Time
                                        where p.Time between '2017' and '2022'
                                          and p.PeopleIncome < pil.LowThreshold
                                        group by p.Province
                                        having COUNT(distinct p.Time) = 6 -- 确保所有六年都在低收入范围内
            )
            select distinct Province
            from LowIncomeProvinces
        end

end;

/* 4.4 */
--比较东部、西部、中部、东北部地区居民收入的增长率
create table #comparison_income(
	Region nvarchar(100),
	Tyear nvarchar(100),
	Income_growthrate float,
	primary key (Region, Tyear)
);
declare @start int, @Income_growthrate float, @Tyear nvarchar(100);
set @start = 2018;
while @start<=2022
begin
    set @Tyear = ltrim(str(@start));
    exec Growthrate '东部地区', 'PeopleIncome_r', @Tyear, @Income_growthrate out;
	insert into #comparison_income 
	values ('东部地区', @Tyear, @Income_growthrate);
    exec Growthrate '西部地区', 'PeopleIncome_r', @Tyear, @Income_growthrate out;
	insert into #comparison_income 
	values ('西部地区', @Tyear, @Income_growthrate);
    exec Growthrate '中部地区', 'PeopleIncome_r', @Tyear, @Income_growthrate out;
	insert into #comparison_income 
	values ('中部地区', @Tyear, @Income_growthrate);
    exec Growthrate '东北地区', 'PeopleIncome_r', @Tyear, @Income_growthrate out;
	insert into #comparison_income 
	values ('东北地区', @Tyear, @Income_growthrate);
	set @start = @start + 1;
end
    
