
--This script calculate the average temperature across the seasons, given season's starting and ending date
-- Do not forget to see the min of Temperature before starting, incase of any -9999 values (null vals.)

--select MIN(TempA)from Observations_History

--2011 winter jan to march
SELECT avg(TempA)as '2011Winter' FROM Observations_history WHERE Date >='2011-01-01' and DATE < '2011-03-21' and TempA !='-9999'

--2011 spring
SELECT avg(TempA) as '2011 Spring' FROM Observations_history WHERE Date >='2011-03-21' and DATE < '2011-06-21' and TempA !='-9999'
--2011 summer
SELECT avg(TempA) as '2011 Summer' FROM Observations_history WHERE Date >='2011-06-21' and DATE < '2011-09-21'and TempA !='-9999'
--2011 fall
SELECT avg(TempA) as '2011 Fall' FROM Observations_history WHERE Date >='2011-09-21' and DATE < '2011-12-21'and TempA !='-9999'
--2011--2012 winter
SELECT avg(TempA) as '2011-2012Winter' FROM Observations_history WHERE Date >='2011-12-21' and DATE < '2012-03-21'and TempA !='-9999'


--2012 spring
SELECT avg(TempA) as '2012 Spring' FROM Observations_history WHERE Date >='2012-03-21' and DATE < '2012-06-21'and TempA !='-9999'
--2012 summer
SELECT avg(TempA) as '2012 Summer' FROM Observations_history WHERE Date >='2012-06-21' and DATE < '2012-09-21'and TempA !='-9999'
--2012 fall
SELECT avg(TempA) as '2012 Fall' FROM Observations_history WHERE Date >='2012-09-21' and DATE < '2012-12-21'and TempA !='-9999'

--2012--2013 winter
SELECT avg(TempA)as '2012-2013 Winter' FROM Observations_history WHERE Date >='2012-12-21' and DATE < '2013-03-21'and TempA !='-9999'


--2013 spring
--SELECT Date,TempA FROM Observations_history WHERE Date >='2013-03-21' and date<=(select MAX(date) from Observations_History) order by DATE desc
SELECT avg(TempA) as '2013 Spring' FROM Observations_history WHERE Date >='2013-03-21' and date<=(select MAX(date) from Observations_History) and TempA !='-9999'