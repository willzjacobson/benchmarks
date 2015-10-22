import nert
import datetime as dt

current = dt.datetime(2014, 1, 15, 2)

while current < dt.datetime(2014, 3, 1):

	print str(current)
	tries = 0
	try:
		nert.search(current)
	except:
		tries += 1
		if tries > 3:
			tries = 0
			current += dt.timedelta(1)
		continue

	current += dt.timedelta(1)
	tries = 0
