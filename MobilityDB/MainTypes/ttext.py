from MobilityDB.TemporalTypes import *


class TTEXT(TEMPORAL):
	BaseValueClass = str

class TTEXTINST(TEMPORALINST, TTEXT):

	def __init__(self, value, time=None):
		super().__init__(value, time)
		TEMPORALINST.BaseValueClass = str

class TTEXTI(TEMPORALI, TTEXT):

	def __init__(self,  *argv):
		super().__init__(*argv)
		TEMPORALI.BaseValueClass = str

class TTEXTSEQ(TEMPORALSEQ, TTEXT):

	def __init__(self, instantList, lower_inc=None, upper_inc=None):
		super().__init__(instantList, lower_inc, upper_inc)
		TEMPORALSEQ.BaseValueClass = str

class TTEXTS(TEMPORALS, TTEXT):

	def __init__(self, *argv):
		super().__init__(*argv)
		TEMPORALS.BaseValueClass = str


