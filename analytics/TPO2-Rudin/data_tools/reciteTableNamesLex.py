# get table names

import lexParameters as pp
import lexParametersNew as ppn

pobj = pp.initializeParametersLex()
pobjNew = ppn.initializeParametersLex()

floorList = pobj.floorList

print "inputs: "
#space Temperature Params
print
print "Space Temperature: "
print "Old Table Names: "

print "ExtendedLogCombinedAll"
print

print "New Table Name: " + pobjNew.sptParams.tableName


#SAT Params
print
print "Supply Air Temperature: "
print "Old Table Names: "
print "ExtendedLogCombinedAll"
print

print "New Table Name: " + pobjNew.satParams.tableName
    

#SAT Params
print
print "return Air Temperature: "
print "Old Table Names: "
print "ExtendedLogCombinedAll"
print

print "New Table Name: " + pobjNew.ratParams.tableName
    


#startup Params
print
print "Startup: "
print "Old Table Names: "
print "ExtendedLogCombinedAll"
print

print "New Table Name: " + str(pobjNew.startupParams.tableName)

#rampdown Params
print
print "rampdown: "
print "Old Table Names: "
print "ExtendedLogCombinedAll"
print

print "New Table Name: " + str(pobjNew.rampdownParams.tableName)

