

class dataRetriever:

	def __init__(self, connection):
	
		self.Connection = connection
		self.Cursor = self.Connection.cursor()
		
		
	def retrieve(self, table, columns=' * ', constraints={}, orderby=[], order='asc', distinct=False):
		
		cols = ''
		if not(isinstance(columns, basestring)):
			last = columns.pop()
			for col in columns:
				cols = cols + '[' + str(col) + ']' + ', '
			cols += '[' + str(last) + ']'
			columns.append(last)
		else:
			cols = columns
			
		query = cols + " FROM " + table
		
		queryConstraints = self.parseConstraints(constraints)
		
		query += queryConstraints
		
		if isinstance(orderby, basestring):
			query += " ORDER BY "
			query += ( "[" + str(orderby) + "]" )
		elif not(orderby == []) and not(orderby == None):
			query += " ORDER BY "
			last = orderby.pop()
			for col in orderby:
				query += ( "[" + str(col) + "]" + ", ")
			query += "[" + last + "]"
			orderby.append(last)
			
		if not(orderby == []) and not(orderby == None) and not(order == 'asc'):
			query += ' DESC '
			
		if distinct == True:
			query = "SELECT DISTINCT " + query
		else:
			query = "SELECT " + query
		
		print query
		self.Cursor.execute(query)
		return self.Cursor.fetchall()
		
		
	def parseConstraints(self, constraints_dictionary):
		
		query = ''
		
		if len(constraints_dictionary) == 0:
			return query
			
		query += " WHERE "
			
		counter1 = 0
		for col in constraints_dictionary:
			counter1 += 1
			query += "( "
			if not(isinstance(constraints_dictionary[col], list)):
				constraints_dictionary[col] = [constraints_dictionary[col]]
			
			counter2 = 0
			for value in constraints_dictionary[col]:
				counter2 += 1
				query += self.toStringConstraint(col, value)
				if not(counter2 == len(constraints_dictionary[col])):
					query += " OR "
			
			query += " )"
			if not(counter1 == len(constraints_dictionary)):
				query += " AND "		
		
		return query

	def toStringConstraint(self, column, value):
		
		if isinstance(value, tuple):
			return "( " + self.singleConstraint(column, value[0] , '>') + " AND " + self.singleConstraint(column, value[1] , '<') + " )"
		else:
			return self.singleConstraint(column, value , '=')
		
	
	def singleConstraint(self, column, value, operator):
		
		if isinstance(value, basestring):
			return str(column) + " " + operator + " " + "\'" + str(value) + "\'"
		else:
			return str(column) + " " + operator + " " + str(value)
