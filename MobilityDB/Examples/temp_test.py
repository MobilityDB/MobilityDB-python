
from parsec import *
from MobilityDB.TemporalTypes.temporal_parser import *
from datetime import datetime, timedelta
from bdateutil.parser import parse
from spans.types import floatrange
from postgis import Geometry, Point, MultiPoint, LineString, GeometryCollection, MultiLineString
from MobilityDB.TimeTypes import TimestampSet, Period, PeriodSet
from MobilityDB.MainTypes import *
from MobilityDB.BoxTypes import *

t = "True"
print("eval", eval(t).__class__)
t = "10"
print("eval", eval(t).__class__)
t = "10.1"
print("eval", eval(t).__class__)

t = True
print (t.__class__)

inst = TBoolInst('True@2000-01-01')
print(inst)

inst = TBoolInst('True', '2000-01-01')
print(inst)

inst = TBoolInst(True, parse('2000-01-01'))
print(inst)

"""
inst = TBoolInst('True', parse('2000-01-01'))
print(inst)
print(inst.BaseClass)
"""




