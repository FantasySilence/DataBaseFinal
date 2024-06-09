create database DataBaseFinal

-- 查看备份文件内容
RESTORE FILELISTONLY
FROM DISK = 'F:\2024-6-9 15-42.bak';

-- 恢复数据库
RESTORE DATABASE DataBaseFinal
FROM DISK = 'F:\2024-6-9 15-42.bak'
WITH REPLACE, -- 覆盖现有数据库
     MOVE 'DataBaseFinal' TO 'xxx\MSSQL16.MSSQLSERVER\MSSQL\DATA\DataBaseFinal.mdf', -- 数据文件的路径
     MOVE 'DataBaseFinal_log' TO 'xxx\MSSQL16.MSSQLSERVER\MSSQL\DATA\DataBaseFinal_log.ldf'; -- 日志文件的路径
     