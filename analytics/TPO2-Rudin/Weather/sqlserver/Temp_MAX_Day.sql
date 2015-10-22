
--This selects date only from datetime with temp values.
--SELECT TempA, Date, cast(Date  as date) DateOnly FROM Observations_History order by DateOnly desc

-- This inserts the above querys output into a table , The table is created before this query is called.
--insert into dbo.Temp_MAX SELECT TempA, Date, cast(Date  as date) DateOnly FROM Observations_History order by DateOnly desc

--This selects the max of tempA with respect to single day. 
--select dateonly, MAX(tempA) from dbo.Temp_MAX group by dateonly

    insert into dbo.Max_Temp_date select dateonly,MAX(tempA) from dbo.Temp_MAX group by dateonly;
