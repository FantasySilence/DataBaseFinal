/* 一些准备工作 */
--查询指定时间指定地区指定经济数据的增长率
create procedure Growthrate
    @area nvarchar(15),
    @data nvarchar(15),
	@year nvarchar(15),
    @result float out
as
begin
    declare @sql nvarchar(max);
	if @area in (select Province from ProvincialInfo)
	    set @sql = N'
		    select @result = (s1.'+@data+'-s2.'+@data+')/s2.'+@data+'
							 from ProvincialInfo s1, ProvincialInfo s2
							 where s1.Province=s2.Province and
							     s1.Province=@area and
							     s1.Time=@year and
								 convert(int, s2.Time)=convert(int, @year)-1
		';
	else if @area in (select Capital from ProvincialCapitalInfo)
	    set @sql = N'
		    select @result = (s1.'+@data+'-s2.'+@data+')/s2.'+@data+'
				             from ProvincialCapitalInfo s1, ProvincialCapitalInfo s2
				             where s1.Capital=s2.Capital and
							     s1.Capital=@area and
							     s1.Time=@year and
								 convert(int, s2.Time)=convert(int, @year)-1
        ';
	else if @area in (select City from MunicipalityInfo)
	    set @sql = N'
		    select @result = (s1.'+@data+'-s2.'+@data+')/s2.'+@data+'
				             from MunicipalityInfo s1, MunicipalityInfo s2
				             where s1.City=s2.City and
							     s1.City=@area and
							     s1.Time=@year and
								 convert(int, s2.Time)=convert(int, @year)-1
        ';
	else if @area in (select EconomicArea from EconomicRegion_view)
	    set @sql = N'
		    select @result = (s1.'+@data+'-s2.'+@data+')/s2.'+@data+'
				             from EconomicRegion_view s1, EconomicRegion_view s2
				             where s1.EconomicArea=s2.EconomicArea and
							     s1.EconomicArea=@area and
							     s1.Time=@year and
								 convert(int, s2.Time)=convert(int, @year)-1
        ';
    exec sp_executesql @sql, 
	    N'@result float output, @year nvarchar(15), @area nvarchar(15)',
        @result=@result output, @year=@year, @area=@area;
end
go

--计算Pearson相关系数
create procedure PearsonCorrelation
    @tableName nvarchar(128),
    @columnX nvarchar(100),
    @columnY nvarchar(100),
	@correlation float out
as
begin
    declare @n int,
            @sumX float,
            @sumY float,
            @sumXY float,
            @sumX2 float,
            @sumY2 float;
    declare @sql nvarchar(max) = N'
        select
            @n = count(*),
            @sumX = sum('+@columnX+'),
            @sumY = sum('+@columnY+'),
            @sumXY = sum('+@columnX+' * '+@columnY+'),
            @sumX2 = sum('+@columnX+' * '+@columnX+'),
            @sumY2 = sum('+@columnY+' * '+@columnY+')
        from '+@tableName;
    exec sp_executesql @sql,
        N'@n int output, @sumX float output, @sumY float output, 
		  @sumXY float output, @sumX2 float output, @sumY2 float output',
        @n output, @sumX output, @sumY output, @sumXY output, @sumX2 output, @sumY2 output;
    set @correlation = (@n*@sumXY - @sumX*@sumY) /
                       sqrt((@n*@sumX2 - @sumX*@sumX) * (@n*@sumY2 - @sumY*@sumY));
end
go

/* 2.1 */
create procedure GDP_Growthrate(
   @start_time int=2018,
   @end_time int=2022,
   @city nvarchar(100)
)
as
begin
    declare @i int, @Tyear nvarchar(50),
	        @province nvarchar(50),
			@GDP_growthrate_city float,
			@GDP_growthrate_province float;
	declare @GDPgrowth_table table(
        City nvarchar(100),
        Province nvarchar(100),
        Tyear nvarchar(100),
        GDP_growthrate_city float,
	    GDP_growthrate_province float,
        primary key (City, Tyear)
    );
	select @i = @start_time, 
	       @province = Province from ProvincialCapital where Capital=@city;
    while @i <= @end_time
    begin
		set @Tyear = ltrim(str(@i));
		exec Growthrate @city, 'GDP', @Tyear, @GDP_growthrate_city out;
		exec Growthrate @province, 'GDP', @Tyear, @GDP_growthrate_province out;
        insert into @GDPgrowth_table
	    values (@city, @province, @Tyear, @GDP_growthrate_city, @GDP_growthrate_province);
		set @i = @i + 1;
	end
	select * from @GDPgrowth_table;
end
go

create procedure GDP_corr(
   @start_time int=2018,
   @end_time int=2022
)
as
begin
    declare @Tyear nvarchar(50),
	        @province nvarchar(50),
			@city nvarchar(50),
			@GDP_corr float;
	create table GDPcorr_table (
        City nvarchar(100),
        Province nvarchar(100),
        GDP_corr float,
        primary key (City)
    );
	declare cur cursor for 
	    select * from ProvincialCapital;
	open cur;
	fetch next from cur into @province, @city;
	while (@@fetch_status=0)
	begin
	    create table #GDPgrowth_table (
	        City nvarchar(100),
			Province nvarchar(100),
			Tyear nvarchar(100),
			GDP_growthrate_city float,
			GDP_growthrate_province float,
			primary key (City, Tyear)
	    ); 
	    insert into #GDPgrowth_table exec GDP_Growthrate @start_time, @end_time, @city;
		exec PearsonCorrelation '#GDPgrowth_table', 'GDP_growthrate_city',
		                        'GDP_growthrate_province', @GDP_corr out;
		insert into GDPcorr_table values(@city, @province, @GDP_corr);
		drop table #GDPgrowth_table;
		fetch next from cur into @province, @city;
	end
	close cur;
	deallocate cur;
end
go

/* 2.2 */
--查询指定时间周期内省会城市人均GDP低于其所在省份的情况
create procedure ComparisonGDP_per
@start_time int=2017, @end_time int=2022
as
    declare @i int, @prov nvarchar(100), @city nvarchar(100),
	        @tyear nvarchar(100), @diffvalue float;
	declare cur_combine cursor for
	    select ProvincialCapital.Province as prov,
		       ProvincialCapital.Capital as city,
		       (ProvincialInfo.GDPperPerson-ProvincialCapitalInfo.GDPperPerson) as diffvalue,
			   ProvincialCapitalInfo.Time as tyear
		from ProvincialCapitalInfo, ProvincialCapital, ProvincialInfo
		where ProvincialCapitalInfo.Capital=ProvincialCapital.Capital and
		      ProvincialCapital.Province=ProvincialInfo.Province and
			  ProvincialCapitalInfo.Time=ProvincialInfo.Time and
			  ProvincialCapitalInfo.Time between @start_time and @end_time;
    select @i = 0;
	open cur_combine;
	fetch next from cur_combine into @prov, @city, @diffvalue, @tyear;
	while (@@fetch_status=0)
	begin
		if @diffvalue > 0
		begin
		    set @i = @i + 1;
			select @tyear + N'年，' + @city + N'的人均GDP低于' + @prov +
				  N'的人均GDP，差值为' + ltrim(str(@diffvalue)) + N'元';
		end
		fetch next from cur_combine into @prov, @city, @diffvalue, @tyear;
	end
	close cur_combine;
	deallocate cur_combine;
	if @i = 0
	    select N'该时间周期内无省会城市人均GDP低于其所在省份的情况';
go

/* 2.3 */
create table comparison_GDP(
    City nvarchar(100),
    Province nvarchar(100),
    Tyear nvarchar(100),
    GDP_growthrate_city float,
	GDP_growthrate_province float,
    primary key (City, Tyear)
);
declare @province nvarchar(100), @city nvarchar(100);
declare cur2 cursor for 
	    select * from ProvincialCapital;
open cur2;
fetch next from cur2 into @province, @city;
while (@@fetch_status=0)
begin
    insert into comparison_GDP
	exec GDP_Growthrate 2018, 2022, @city;
    fetch next from cur2 into @province, @city;
end
close cur2;
deallocate cur2;
go

create view GDP_DUD as
    select s1.Province, s1.City 
	from comparison_GDP s1, comparison_GDP s2, comparison_GDP s3
	where s1.Tyear='2020' and s1.Tyear='2021' and s1.Tyear='2022' and
	      s1.City=s2.City and s2.City=s3.City and
		  s1.GDP_growthrate_province<0 and s2.GDP_growthrate_province>0 and
		  s3.GDP_growthrate_province<0;
go

create view GDP_DDD_city as
    select s1.Province, s1.City 
	from comparison_GDP s1, comparison_GDP s2, comparison_GDP s3
	where s1.Tyear='2020' and s2.Tyear='2021' and s3.Tyear='2022' and
	      s1.City=s2.City and s2.City=s3.City and
		  s1.City in (select City from GDP_DUD) and
		  s1.GDP_growthrate_city>0 and s2.GDP_growthrate_city>0 and
		  s3.GDP_growthrate_city>0;
go


/* 2.4 */
create procedure TopGDP
    @Area nvarchar(50)= N'高',
    @start_time nvarchar(50) = '2018',
    @end_time nvarchar(50) = '2018'
as
	if @Area = N'高'
		select top(3) City, Province, GDP_growthrate_city, GDP_growthrate_province from Comparison_GDP
		where Tyear between @start_time and @end_time
		order by GDP_growthrate_city desc;
	else if @Area = N'低'
		select top(3) City, Province, GDP_growthrate_city, GDP_growthrate_province from Comparison_GDP
		where Tyear between @start_time and @end_time
		order by GDP_growthrate_city;
go
