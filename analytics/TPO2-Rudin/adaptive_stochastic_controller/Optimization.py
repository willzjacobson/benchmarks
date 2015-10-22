
import datetime as dt

import numpy

def startup(df):
	l = []
	for i in df.group['fan']:
		for j in xrange(df.pointSize-1):
			if df.X.T[i][j+1] == 1 and df.X.T[i][j] == 0:
				if df.timestamps[j].hour > 4 and df.timestamps[j].hour < 7: 
					l.append(df.timestamps[j])
				break
	index = int(0.2*len(l))
	return sorted(l)[index]

def preheat(df):
	l = []
	for i in df.group['pump']:
		for j in xrange(df.pointSize-1):
			if df.X.T[i][j+1] == 1 and df.X.T[i][j] == 0:
				if df.timestamps[j].hour > 4 and df.timestamps[j].hour < 7: 
					l.append(df.timestamps[j])
				break

	print l


def cost(df, factorize=False):

	tau = numpy.random.rand(24)
	eta = numpy.random.rand(24)
	sigma = numpy.random.rand(24)

	opening_hour = 7
	closing_hour =  19

	granularity = 15

	Cost = 0

	temp_violation = 0
	temp_penalty = 0
	steam_cost = 0
	electric_cost = 0
	energy_cost = 0

	for i in xrange(24):

		if i >=6 and i < 19:
			sigma[i] = 10 * 26.5 * granularity/60
		else:
			sigma[i] = 26.5 * granularity/60 

		eta[i] = 0.2 * granularity/60

		if i >= 7 and i < 19:
			tau[i] = 1000
		else:
			tau[i] = 0

	for t in xrange(df.pointSize):
		hour = df.timestamps[t].hour

		for i in df.group['temp']:
			violation = 0
			temp = df.X[t, i]
			if temp >= 72 and temp <= 75:
				violation = 0
			elif temp >= 70 and temp <= 77:
				violation = 20 * min([abs(77-temp), abs(72-temp)])
			else:
				violation = 100 * min([abs(77-temp), abs(72-temp)])
	
			temp_penalty += tau[hour] * violation * violation 

			
			violation = 0
			temp = df.X[t, i]
			if temp >= 72 and temp <= 75:
				violation = 0		
			else:
				violation = min([abs(75-temp), abs(72-temp)])
			temp_violation += (tau[hour]/1000) * violation/len(df.group['temp']) /4*12
		
	
		

		for i in df.group['electric']:
			electric_cost += eta[hour] * df.X[t, i]

		for i in df.group['steam']:
			steam_cost += sigma[hour] * df.X[t, i]

	energy_cost = steam_cost + electric_cost

	alpha = 1
	beta = 1

	objective = energy_cost + temp_penalty

	if factorize:
		return [temp_penalty, temp_violation, electric_cost, steam_cost, energy_cost, objective]
	else:
		return objective


# parameters:
#	hdf: history dataframe
#	cdf: current dataframe which contains the current dataforecast as of now
#	model: response model
def search(hdf, cdf, model):


	i_history = []
	i_current = []
	for name in cdf.pointnames:
		if cdf.pointnames.index(name) in cdf.group['weather'] or cdf.pointnames.index(name) in cdf.group['time']:
			continue
		else:
			i_history.append(hdf.pointnames.index(name))
			i_current.append(cdf.pointnames.index(name))


	t = hdf.pointnames.index('minute')	
	for j in range(0, len(hdf.X.T[t])):
		if hdf.X.T[t][j] == cdf.X.T[cdf.pointnames.index('minute')][0]:
			dayPointer = j
			break

	costs = []
	actionPointers = []
	# traversing through all weekdays to find potential actions
	# keeps costs in a list then picks the best cost and corresponding action
	while dayPointer + 24 * 4 + 1 < hdf.pointSize:
		#print str(hdf.timestamps[dayPointer])
		if hdf.timestamps[dayPointer].weekday() == 5 or hdf.timestamps[dayPointer].weekday() == 6:
			dayPointer += 24 * 4
			continue

		for i_h, i_c in zip(i_history, i_current):
			cdf.X.T[i_c] = hdf.X.T[i_h][dayPointer:dayPointer+cdf.pointSize]

		#rdf = model.predict(hdf.timestamps[-1], hdf.X[-1], cdf)
		rdf = model.predict(cdf.timestamps[0]-dt.timedelta(0, 15*60), hdf.X[-1], cdf)

		costs.append(cost(rdf))
		actionPointers.append(dayPointer)

		dayPointer += 24 * 4

	bestActionPointer = actionPointers[costs.index(min(costs))]

	for i_h, i_c in zip(i_history, i_current):
		cdf.X.T[i_c] = hdf.X.T[i_h][bestActionPointer:bestActionPointer+cdf.pointSize]

	bestDF = model.predict(cdf.timestamps[0]-dt.timedelta(0, 15*60), hdf.X[-1], cdf)

	return bestDF


