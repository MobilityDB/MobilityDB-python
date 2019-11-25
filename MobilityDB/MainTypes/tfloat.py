from MobilityDB.TemporalTypes import *


class TFLOAT(TEMPORAL):
	BaseValueClass = float

class TFLOATINST(TEMPORALINST, TFLOAT):
	def __init__(self, value, time=None):
		super().__init__(value, time)
		TEMPORALINST.BaseValueClass = float


class TFLOATI(TEMPORALI, TFLOAT):
	def __init__(self,  *argv):
		super().__init__(*argv)
		TEMPORALI.BaseValueClass = float

class TFLOATSEQ(TEMPORALSEQ, TFLOAT):
	def __init__(self, instantList, lower_inc=None, upper_inc=None):
		super().__init__(instantList, lower_inc, upper_inc)
		TEMPORALSEQ.BaseValueClass = float

class TFLOATS(TEMPORALS, TFLOAT):
	def __init__(self, *argv):
		super().__init__(*argv)
		TEMPORALS.BaseValueClass = float
