# get table names

import parkParameters as pp
import parkParametersNew as ppn

pobj = pp.initializeParametersPark()
pobjNew = ppn.initializeParametersPark()

floorList = pobj.floorList

print "inputs: "
#space Temperature Params
print
print "Space Temperature: "
print "Old Table Names: "

print pobj.sptParams.tableNameList
print

print "New Table Name: " + pobjNew.sptParams.tableName


#SAT Params
print
print "Supply Air Temperature: "
print "Old Table Names: "
print pobj.satParams.tableNameList
print

print "New Table Name: " + pobjNew.satParams.tableName
    
#startup Params
print
print "Startup: "
print "Old Table Names: "
print pobj.startupParams.tableNameList 
print

print "New Table Name: " + str(pobjNew.startupParams.tableNameList)

#rampdown Params
print
print "rampdown: "
print "Old Table Names: "
print pobj.rampdownParams.tableName
print

print "New Table Name: " + str(pobjNew.rampdownParams.tableName)
