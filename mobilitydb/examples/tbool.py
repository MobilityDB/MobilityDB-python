###############################################################################
#
# This MobilityDB code is provided under The PostgreSQL License.
#
# Copyright (c) 2019-2022, Université libre de Bruxelles and MobilityDB
# contributors
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose, without fee, and without a written 
# agreement is hereby granted, provided that the above copyright notice and
# this paragraph and the following two paragraphs appear in all copies.
#
# IN NO EVENT SHALL UNIVERSITE LIBRE DE BRUXELLES BE LIABLE TO ANY PARTY FOR
# DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING
# LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION,
# EVEN IF UNIVERSITE LIBRE DE BRUXELLES HAS BEEN ADVISED OF THE POSSIBILITY 
# OF SUCH DAMAGE.
#
# UNIVERSITE LIBRE DE BRUXELLES SPECIFICALLY DISCLAIMS ANY WARRANTIES, 
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER IS ON
# AN "AS IS" BASIS, AND UNIVERSITE LIBRE DE BRUXELLES HAS NO OBLIGATIONS TO 
# PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS. 
#
###############################################################################

from datetime import datetime, timedelta
from dateutil.parser import parse
from mobilitydb.time import TimestampSet, Period, PeriodSet
from mobilitydb.main import TBoolInst, TBoolInstSet, TBoolSeq, TBoolSeqSet


print("\nConstructors for TBoolInst")
inst = TBoolInst('True@2019-09-08')
print(inst)
inst = TBoolInst('True', '2019-09-08')
print(inst)
t = parse('2019-09-08')
inst = TBoolInst('True', t)
print(inst)

print("\nConstructors for TBoolInstSet")
ti = TBoolInstSet('{True@2019-09-08, False@2019-09-09, False@2019-09-10}')
print(tinstset)
ti = TBoolInstSet('True@2019-09-08', 'False@2019-09-09', 'False@2019-09-10')
print(tinstset)
ti = TBoolInstSet(['True@2019-09-08', 'False@2019-09-09', 'False@2019-09-10'])
print(tinstset)
t1 = TBoolInst('True@2019-09-08')
t2 = TBoolInst('False@2019-09-09')
t3 = TBoolInst('False@2019-09-10')
ti = TBoolInstSet(t1, t2, t3)
print(tinstset)
ti = TBoolInstSet([t1, t2, t3])
print(tinstset)

print("\nConstructors for TBoolSeq")
seq = TBoolSeq('[True@2019-09-08, False@2019-09-09, False@2019-09-10]')
print(seq)
seq = TBoolSeq(['True@2019-09-08', 'False@2019-09-09', 'False@2019-09-10'])
print(seq)
seq = TBoolSeq([t1, t2, t3])
print(seq)
seq = TBoolSeq([t1, t2, t3], False, True)
print(seq)

print("\nConstructors for TBoolSeqSet")
ts = TBoolSeqSet('{[True@2019-09-08, False@2019-09-09, False@2019-09-10],[False@2019-09-11, True@2019-09-12]}')
print(ts)
ts = TBoolSeqSet(['[True@2019-09-08, False@2019-09-09, False@2019-09-10]', '[False@2019-09-11, True@2019-09-12]'])
print(ts)
seq1 = TBoolSeq('[True@2019-09-08, False@2019-09-09, False@2019-09-10]')
seq2 = TBoolSeq('[False@2019-09-11, True@2019-09-12]')
ts = TBoolSeqSet([seq1, seq2])
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

print("\ntempSubtype")
print(inst.tempSubtype())
print(ti.tempSubtype())
print(seq.tempSubtype())
print(ts.tempSubtype())

print("\ninterpolation")
print(seq.interpolation)
print(ts.interpolation)

print("\ngetValue")
print(inst.getValue)

print("\ngetValues")
print(inst.getValues)
print(ti.getValues)
print(seq.getValues)
print(ts.getValues)

print("\nstartValue")
print(inst.startValue)
print(ti.startValue)
print(seq.startValue)
print(ts.startValue)

print("\nendValue")
print(inst.endValue)
print(ti.endValue)
print(seq.endValue)
print(ts.endValue)

print("\nminValue")
print(inst.minValue)
print(ti.minValue)
print(seq.minValue)
print(ts.minValue)

print("\nmaxValue")
print(inst.maxValue)
print(ti.maxValue)
print(seq.maxValue)
print(ts.maxValue)

print("\ngetTimestamp")
print(inst.getTimestamp)

print("\ngetTime")
print(inst.getTime)
print(ti.getTime)
print(seq.getTime)
print(ts.getTime)

print("\nduration")
print(inst.duration)
print(ti.duration)
print(seq.duration)
print(ts.duration)

print("\ntimespan")
print(inst.timespan)
print(ti.timespan)
print(seq.timespan)
print(ts.timespan)

print("\nperiod")
print(inst.period)
print(ti.period)
print(seq.period)
print(ts.period)

print("\nnumInstants")
print(inst.numInstants)
print(ti.numInstants)
print(seq.numInstants)
print(ts.numInstants)

print("\nstartInstant")
print(inst.startInstant)
print(ti.startInstant)
print(seq.startInstant)
print(ts.startInstant)

print("\nendInstant")
print(inst.endInstant)
print(ti.endInstant)
print(seq.endInstant)
print(ts.endInstant)

print("\ninstantN")
print(inst.instantN(1))
print(ti.instantN(1))
print(seq.instantN(1))
print(ts.instantN(1))

print("\ninstants")
print(inst.instants)
print(ti.instants)
print(seq.instants)
print(ts.instants)

print("\nnumTimestamps")
print(inst.numTimestamps)
print(ti.numTimestamps)
print(seq.numTimestamps)
print(ts.numTimestamps)

print("\nstartTimestamp")
print(inst.startTimestamp)
print(ti.startTimestamp)
print(seq.startTimestamp)
print(ts.startTimestamp)

print("\nendTimestamp")
print(inst.endTimestamp)
print(ti.endTimestamp)
print(seq.endTimestamp)
print(ts.endTimestamp)

print("\ntimestampN")
print(inst.timestampN(1))
print(ti.timestampN(1))
print(seq.timestampN(1))
print(ts.timestampN(1))

print("\ntimestamps")
print(inst.timestamps)
print(ti.timestamps)
print(seq.timestamps)
print(ts.timestamps)

print("\nnumSequences")
print(seq.numSequences)
print(ts.numSequences)

print("\nstartSequence")
print(seq.startSequence)
print(ts.startSequence)

print("\nendSequence")
print(seq.endSequence)
print(ts.endSequence)

print("\nsequenceN")
print(seq.sequenceN(1))
print(ts.sequenceN(1))

print("\nsequences")
print(seq.sequences)
print(ts.sequences)

print("\nshift")
print(inst.shift(timedelta(days=1)))
print(ti.shift(timedelta(days=1)))
print(seq.shift(timedelta(days=1)))
print(ts.shift(timedelta(days=1)))

print("\nintersectsTimestamp")
t = datetime.strptime('2019-09-09', '%Y-%m-%d')
print(inst.intersectsTimestamp(t))
print(ti.intersectsTimestamp(t))
print(seq.intersectsTimestamp(t))
print(ts.intersectsTimestamp(t))

print("\nintersectsTimestampSet")
tss = TimestampSet('{2019-09-09, 2019-09-10}')
print(inst.intersectsTimestampSet(tss))
print(ti.intersectsTimestampSet(tss))
print(seq.intersectsTimestampSet(tss))
print(ts.intersectsTimestampSet(tss))

print("\nintersectsPeriod")
p = Period('2019-09-09', '2019-09-10', True, True)
print(inst.intersectsPeriod(p))
print(ti.intersectsPeriod(p))
print(seq.intersectsPeriod(p))
print(ts.intersectsPeriod(p))

print("\nintersectsPeriodSet")
ps = PeriodSet('{[2019-09-09,2019-09-10], [2019-09-11,2019-09-12]}')
print(inst.intersectsPeriodSet(ps))
print(ti.intersectsPeriodSet(ps))
print(seq.intersectsPeriodSet(ps))
print(ts.intersectsPeriodSet(ps))
