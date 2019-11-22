from MobilityDB.TemporalTypes import *


class TFLOAT(TEMPORAL):
	BaseValueClass = float

class TFLOATINST(TEMPORALINST, TFLOAT):
	def __init__(self, value, time=None):
		super().__init__(value, time)

class TFLOATI(TEMPORALI, TFLOAT):
	def __init__(self, value, time=None):
		super().__init__(value, time)

class TFLOATSEQ(TEMPORALSEQ, TFLOAT):
	def __init__(self, value, time=None):
		super().__init__(value, time)

class TFLOATS(TEMPORALS, TFLOAT):
	def __init__(self, value, time=None):
		super().__init__(value, time)
