--select * from dbo.Observations_History
-- truncate table dbo.Observations_History
--select max(Date) as max_date from dbo.Observations_History
--select COUNT(*) from dbo.Observations_History

--SELECT [Date] FROM dbo.Observations_History GROUP BY [Date] --This gives the unique  values comparing the Column values of [Date] column

--select * into dbo.Observations_bckp_aftr_edt_datatypes2 from dbo.Observations_History -- this creates a backup table and copies all the data into it. 

--select * from dbo.Observations_History
--select * from dbo.Hourly_Forecast
--select * from dbo.Observations_History_backup_bfr_datatypeschng
--select * from dbo.Observations_History where Humidity is null

--select Run_DateTime,Date from [Weather].[dbo].[Observations_History] where Run_DateTime like '2013-04-25%' order by Run_DateTime desc

--select max(Date) FROM dbo.Observations_History
