class Error(Exception):
	pass

class UnsuportedRasterVariableError(Error):
	def __init__(self, variableNames):
		print 'file Variables', variableNames, 'not supported'
