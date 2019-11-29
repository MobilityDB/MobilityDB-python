from MobilityDB.TemporalTypes import *


class TBOOL(TEMPORAL):
	BaseValueClass = bool

class TBOOLINST(TEMPORALINST, TBOOL):

	def __init__(self, value, time=None):
		TEMPORALINST.BaseValueClass = str
		super().__init__(value, time)

class TBOOLI(TEMPORALI, TBOOL):

	def __init__(self,  *argv):
		TEMPORALI.BaseValueClass = str
		TEMPORALI.ComponentValueClass = TBOOLINST
		super().__init__(*argv)

class TBOOLSEQ(TEMPORALSEQ, TBOOL):

	def __init__(self, instantList, lower_inc=None, upper_inc=None):
		TEMPORALSEQ.BaseValueClass = str
		TEMPORALSEQ.ComponentValueClass = TBOOLINST
		super().__init__(instantList, lower_inc, upper_inc)

class TBOOLS(TEMPORALS, TBOOL):

	def __init__(self, *argv):
		TEMPORALS.BaseValueClass = str
		TEMPORALS.ComponentValueClass = TBOOLSEQ
		super().__init__(*argv)


