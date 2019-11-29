from MobilityDB import *
from bdateutil.parser import parse
from spans.types import Range

class intrange(Range):
	__slots__ = ()
	type = int

inst = TIntInst('10@2019-09-08')
print(inst)
inst = TIntInst('10', '2019-09-08')
print(inst)
t = parse('2019-09-08')
inst = TIntInst(10, t)
print(inst)
ti = TIntI('{10@2019-09-08, 20@2019-09-09, 20@2019-09-10}')
print(ti)
seq = TIntSeq('[10@2019-09-08, 20@2019-09-09, 20@2019-09-10]')
print(seq)
ts = TIntS('{[10@2019-09-08, 20@2019-09-09, 20@2019-09-10],[25@2019-09-11, 30@2019-09-12]}')
print(ts)

print("\n__class__ ")
print(inst.__class__.__name__)
print(ti.__class__.__name__)
print(seq.__class__.__name__)
print(ts.__class__.__name__)

print("\n__bases__ ")
print(inst.__class__.__bases__)
print(ti.__class__.__bases__)
print(seq.__class__.__bases__)
print(ts.__class__.__bases__)

print("\nduration")
print(inst.duration())
print(ti.duration())
print(seq.duration())
print(ts.duration())

print("\ngetValue")
print(inst.getValue())

print("\ngetValues")
print(inst.getValues())
print(ti.getValues())
print(seq.getValues())
print(ts.getValues())

print("\nstartValue")
print(inst.startValue())
print(ti.startValue())
print(seq.startValue())
print(ts.startValue())

print("\nendValue")
print(inst.endValue())
print(ti.endValue())
print(seq.endValue())
print(ts.endValue())

print("\nminValue")
print(inst.minValue())
print(ti.minValue())
print(seq.minValue())
print(ts.minValue())

print("\nmaxValue")
print(inst.maxValue())
print(ti.maxValue())
print(seq.maxValue())
print(ts.maxValue())

print("\nvalueRange")
print(inst.valueRange())
print(ti.valueRange())
print(seq.valueRange())
print(ts.valueRange())

print("\ngetTimestamp")
print(inst.getTimestamp())

print("\ngetTime")
print(inst.getTime())
print(ti.getTime())
print(seq.getTime())
print(ts.getTime())

print("\ntimespan")
print(inst.timespan())
print(ti.timespan())
print(seq.timespan())
print(ts.timespan())

print("\nperiod")
print(inst.period())
print(ti.period())
print(seq.period())
print(ts.period())

print("\nnumInstants")
print(inst.numInstants())
print(ti.numInstants())
print(seq.numInstants())
print(ts.numInstants())

print("\nstartInstant")
print(inst.startInstant())
print(ti.startInstant())
print(seq.startInstant())
print(ts.startInstant())

print("\nendInstant")
print(inst.endInstant())
print(ti.endInstant())
print(seq.endInstant())
print(ts.endInstant())

print("\ninstantN")
print(inst.instantN(1))
print(ti.instantN(1))
print(seq.instantN(1))
print(ts.instantN(1))

print("\ninstants")
print(inst.instants())
print(ti.instants())
print(seq.instants())
print(ts.instants())

print("\nnumTimestamps")
print(inst.numTimestamps())
print(ti.numTimestamps())
print(seq.numTimestamps())
print(ts.numTimestamps())

print("\nstartTimestamp")
print(inst.startTimestamp())
print(ti.startTimestamp())
print(seq.startTimestamp())
print(ts.startTimestamp())

print("\nendTimestamp")
print(inst.endTimestamp())
print(ti.endTimestamp())
print(seq.endTimestamp())
print(ts.endTimestamp())

print("\ntimestampN")
print(inst.timestampN(1))
print(ti.timestampN(1))
print(seq.timestampN(1))
print(ts.timestampN(1))

print("\ntimestamps")
print(inst.timestamps())
print(ti.timestamps())
print(seq.timestamps())
print(ts.timestamps())

