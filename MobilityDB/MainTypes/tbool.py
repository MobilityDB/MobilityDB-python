from MobilityDB.TemporalTypes import *


class TBool(Temporal):
	BaseValueClass = bool

class TBoolInst(TemporalInst, TBool):

	def __init__(self, value, time=None):
		TemporalInst.BaseValueClass = str
		super().__init__(value, time)

class TBoolI(TemporalI, TBool):

	def __init__(self,  *argv):
		TemporalI.BaseValueClass = str
		TemporalI.ComponentValueClass = TBoolInst
		super().__init__(*argv)

class TBoolSeq(TemporalSeq, TBool):

	def __init__(self, instantList, lower_inc=None, upper_inc=None):
		TemporalSeq.BaseValueClass = str
		TemporalSeq.ComponentValueClass = TBoolInst
		super().__init__(instantList, lower_inc, upper_inc)

class TBoolS(TemporalS, TBool):

	def __init__(self, *argv):
		TemporalS.BaseValueClass = str
		TemporalS.ComponentValueClass = TBoolSeq
		super().__init__(*argv)


