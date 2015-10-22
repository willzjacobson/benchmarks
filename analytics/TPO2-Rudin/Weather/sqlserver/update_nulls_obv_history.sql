--use dbo.Observations_History;

update dbo.Observations_History set WindGustA ='-9999' where WindGustA < '-900';
--update dbo.Observations_History set WindGustA ='-9999' where WindGustA is null 

update dbo.Observations_History set WindGustM = '-9999' where WindGustM < '-900';
--update dbo.Observations_History set WindGustM = '-9999' where WindGustM is null

update dbo.Observations_History set HeatIndexA = '-9999' where HeatIndexA < '-900';
--update dbo.Observations_History set HeatIndexA = '-9999' where HeatIndexA is null

update dbo.Observations_History set HeatIndexM ='-9999' where HeatIndexM < '-900';
--update dbo.Observations_History set HeatIndexM ='-9999' where HeatIndexM is null

update dbo.Observations_History set PrecipA = '-9999' where PrecipA < '-900';
--update dbo.Observations_History set PrecipA = '-9999' where PrecipA is null

update dbo.Observations_History set PrecipM = '-9999' where PrecipM < '-900';
--update dbo.Observations_History set PrecipM = '-9999' where PrecipM is null

update dbo.Observations_History set WindChillA = '-9999' where WindChillA <'-900';
--update dbo.Observations_History set WindChillA = '-9999' where WindChillA is null

update dbo.Observations_History set WindChillM = '-9999' where WindChillM <'-900';
--update dbo.Observations_History set WindChillM = '-9999' where WindChillM is null

--select * from dbo.Observations_History where HeatIndexA is not null
--select * from dbo.Observations_History
