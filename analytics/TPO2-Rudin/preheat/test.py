
from dbInterface import dbInterface
import datetime as dt

end = dt.datetime.now()
start = end - dt.timedelta(10)

i = dbInterface()

print i.getAverageTemperature(end)
print i.getCurrentSteamSeries(start,end)
#i.commitForecast(datetime.datetime.now())
