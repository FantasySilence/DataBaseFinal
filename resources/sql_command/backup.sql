/* 备份 */
create proc back_up @savepath nvarchar(max)
as
    backup database DataBaseFinal to disk = @savepath
go;

/* 回档 */
create proc restore_
    @backup_path nvarchar(200), @data_path nvarchar(200),
    @log_path nvarchar(200)
as
    restore database DataBaseFinal
    from disk =  @backup_path with replace,
    move 'DataBaseFinal' to @data_path,
    move 'DataBaseFinal_log' to @log_path
go;
     