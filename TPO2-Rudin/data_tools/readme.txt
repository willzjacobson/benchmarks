data-tools readme:
These data tools were built for the purpose of allowing you easy access to building management data for
the SELEX/Rudin project

A list of the modules:

1) dataCollectors.py
	- This file contains the code for the various dataCollector objects that have been built to interface
	  with the databases on Bucky, Bell (deprecated), and newer databases on the 32 AA VM and (equivalently)
	  those on anderson

	- Use these objects as the containers for your data.  They are all built with a similar philosophy:
		To allow you simple access to the data using parameters gathered and built from either the 
		config file (for the newer data collectors), or from hard coded parameter config python
		scripts, and stored in a parameter object.  In using them, you will not have to worry about
		writing queries; rather, you can work with data in a recognizable and regular fashion

		Because the move to 32 AA has been slowed down, and because we do not have the tables switched
		to the Anderson, you may have to use the older dataCollectors (noted as deprecated in the comments)
		
	- Instructions:
		Every data collector is inherited from the base class, dataCollectorBase.  The dataCollectorBase's
		constructor is informative, as it highlights all of the base attributes of the dataCollector.

		The constructor for dataCollectorBase is:
		
		dataCollectorBase(conn, cursor, tablename, numberOfDays, startDatetime, includeweekends)

			- conn: the connection to the database via the pyodbc sql driver
			- cursor: the cursor object for the pyodbc driver
			- tableName: the name of the table to query (parameterized by parameter object)
			- numberOfDays: the number of days of data  to query from the past ( starting 
					from the day specified in the startDatetime parameter)
			- startDatetime: a python datetime object which gives the date and time from which
					to start querying data.  Data is always queried in the past
			- includeWeekends: a True/False parameter, setting whether weekend data should
					  be included in the query.


			Once the data is queried, it is stored in one of two dictionaries:

			- rawDataKeyDayKeyFloor OR rawDataKeyDay.  The naming scheme should allow you to 
			   remember how to access data in the correct fashion =)

			rawDataKeyDayKeyFloor has the structure:
				rawDataKeyDayKeyFloor[datetime.day][floor (e.g. 'F04')] = [(datetime.datetime, value), ...]
				
				that is, when you provide a day and a floor, you access a list of tuples
				with the first value being the timestamp, the second being the value

			rawDataKeyDay has the structure:
				rawDataKeyDay[datetime.day] = [(datetime.datetime, value), ...]
	
				that is, when you provide a day, you access a list of tuples with the first
				value being the timestamp, the second being the value


			If you query data that is floor based, you will get an output of rawDataKeyDayKeyFloor,
			otherwise you will get an output rawDataKeyDay

		dataCollectorBMSInput:

		The dataCollectorBMSInput is the second relevant data collector that you should be aware of.
		It is built to be compatible with the data stored in the new databases, and thus follows the 
		regularized schema design to be implemented with all new building expansions.  Along with the
		parameters mentioned for dataCollectorBase, the dataCollectorBMSInput uses two more parameters
		in its constructor:

			- equalityConstraintList: this defaults to ['*'], a list with a single wildcard character.
			  The equality constraint list designates the terms that you wish to scope to certain 
			  values via an equality join.  This means, if I have 
								equalityConstraintList = ['FLOOR', 'QUADRANT'],
			  it means that I wish to perform queries ensuring certain values of floor and quandrant.

			- constraintValListKeyFloor: This dictionary works with the equalityConstraintList by 
			  assigning the appropriate values for the terms in the equalityConstraintList for 
			  given floors; the choice of floors as the key to the dictionary seemed like the best
			  at the time, because we are often either using building-wide data (steam/electricity),
			  or are using floor specific data, or data that can be connected with a floor (supply
			  air temperature, or space temperature).  
				Following the above example, if I have
				constraintValListKeyFloor = {'F02': ['F02', 'CNW'], 'F04' : ['F04', 'CSW']}, 
				that means that I will perform two queries: the first will be to select data 
				with the equality constraints "Floor = 'F02' and Quadrant = 'CNW"
										AND
								"Floor = 'F04' and Quadrant = 'CSW'"

			It is worth noting that if you are querying from a table without equality constraints
			(i.e. not floor specific data), one should simply leave the values of 
			equalityConstraintList and constraintValListKeyFloor as their default values

2.) park/lex parameters:

	The parameter objects interface with the dataCollector modules in a very straightforward fashion.

	If you are using a data collector to access space temperature data, the relevant space temperature 
	parameters are in the parameter object paramObj.sptparams, and match the constructor parameter 
	requirements verbatum
								