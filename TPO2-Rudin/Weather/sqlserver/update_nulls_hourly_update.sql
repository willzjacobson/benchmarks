--use dbo.Hourly_Forcast;

update dbo.Hourly_Forecast set HeatIndexA ='-9999' where HeatIndexA < '-50'
update dbo.Hourly_Forecast set WX = '-9999' where WX =''
update dbo.Hourly_Forecast set HeatIndexM = '-9999' where HeatIndexM < '-50'
update dbo.Hourly_Forecast set WindChillA =  '-9999' where WindChillA < '-50'
update dbo.Hourly_Forecast set WindChillM = '-9999' where WindChillM < '-50'


--select * from dbo.Hourly_Forecast where HeatIndexA= '-9999'
--select * into dbo.Hourly_Forecast_bck from dbo.Hourly_Forecast -- this creates a backup table and copies all the data into it. 