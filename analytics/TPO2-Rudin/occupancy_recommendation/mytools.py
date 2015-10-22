import pyodbc
import datetime
import time
import numpy

def wrapString(string, char):
	
    if char == "(" or char == ")":
	return "(" + string + ")"
    elif char == "[" or char == "]":
	return "[" + string + "]"
    elif char == "{" or char == "}":
	return "{" + string + "}"
		
    else:
	return char + string + char


def connectionString(server, database, uid, pwd):
    
    return "DRIVER={SQL SERVER};SERVER=" + server + ";DATABASE=" + database + ";uid=" + uid + ";pwd=" + pwd


def connectTo(server, database, uid, pwd):

    try:
	print "Initiating connection to " + server	
	return pyodbc.connect(connectionString(server, database, uid, pwd))
    except:
	
	print "Connection to " + server + " failed"


def datetimeInterval(beginDate, endDate, step):

    datetimeList = []

    current = beginDate
    while(current < endDate):
	datetimeList.append(current)
	current += step

    return datetimeList


strptime = lambda date_string, format: datetime.datetime(*(time.strptime(date_string, format)[0:6]))



# timesereis : dict<datetime, [scalar, array]>, desired: list<datetime>, degree: int
def interpolateTimeseries(timeseries, desired, degree=1):

    new_timeseries = {}

    original_timestamps = sorted(timeseries.keys())
    target_timestamps = sorted(desired)


    for timestamp in target_timestamps:
	
	interval = findWrap(original_timestamps, timestamp)
	first = interval[0]
	last = interval[1]

	if (first == last):
	    new_timeseries[timestamp] = timeseries[first]
	    continue

	if (degree == 0):
	    new_timeseries[timestamp] = timeseries[first]
	    continue

	alpha = (last - timestamp).seconds*1.0/(last - first).seconds
	beta = (timestamp - first).seconds*1.0/(last - first).seconds

	new_timeseries[timestamp] = list(alpha*numpy.array(timeseries[first]) + beta*numpy.array(timeseries[last]))


    return new_timeseries

def findWrap(sorted_list, element):
    
    if element > sorted_list[-1]:
	return (sorted_list[-1], sorted_list[-1])

    elif element < sorted_list[0]:
	return (sorted_list[0], sorted_list[0])

    else:
	first = 0
	last = len(sorted_list) - 1
	while not(last - first <= 1):
 
	    mid = (last + first)/2
	    
	    if element <= sorted_list[mid]:
		last = mid

	    elif element >= sorted_list[mid]:
		first = mid

    return (sorted_list[first], sorted_list[last])
