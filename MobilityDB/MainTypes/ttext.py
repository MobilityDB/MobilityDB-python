from MobilityDB.TemporalTypes import *


class TText(Temporal):
	BaseValueClass = str

class TTextInst(TemporalInst, TText):

	def __init__(self, value, time=None):
		TemporalInst.BaseValueClass = str
		super().__init__(value, time)

class TTextI(TemporalI, TText):

	def __init__(self,  *argv):
		TemporalI.BaseValueClass = str
		TemporalI.ComponentValueClass = TTextInst
		super().__init__(*argv)

class TTextSeq(TemporalSeq, TText):

	def __init__(self, instantList, lower_inc=None, upper_inc=None):
		TemporalSeq.BaseValueClass = str
		TemporalSeq.ComponentValueClass = TTextInst
		super().__init__(instantList, lower_inc, upper_inc)

class TTextS(TemporalS, TText):

	def __init__(self, *argv):
		TemporalS.BaseValueClass = str
		TemporalS.ComponentValueClass = TTextSeq
		super().__init__(*argv)


