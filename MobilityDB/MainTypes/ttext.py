from MobilityDB.TemporalTypes import *


class TTEXT(TEMPORAL):
	BaseValueClass = str

class TTEXTINST(TEMPORALINST, TTEXT):

	def __init__(self, value, time=None):
		TEMPORALINST.BaseValueClass = str
		super().__init__(value, time)

class TTEXTI(TEMPORALI, TTEXT):

	def __init__(self,  *argv):
		TEMPORALI.BaseValueClass = str
		TEMPORALI.ComponentValueClass = TTEXTINST
		super().__init__(*argv)

class TTEXTSEQ(TEMPORALSEQ, TTEXT):

	def __init__(self, instantList, lower_inc=None, upper_inc=None):
		TEMPORALSEQ.BaseValueClass = str
		TEMPORALSEQ.ComponentValueClass = TTEXTINST
		super().__init__(instantList, lower_inc, upper_inc)

class TTEXTS(TEMPORALS, TTEXT):

	def __init__(self, *argv):
		TEMPORALS.BaseValueClass = str
		TEMPORALS.ComponentValueClass = TTEXTSEQ
		super().__init__(*argv)


