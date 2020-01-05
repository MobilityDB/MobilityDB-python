
from parsec import *
from MobilityDB.TemporalTypes.temporal_parser import *
from datetime import datetime, timedelta
from bdateutil.parser import parse
from spans.types import floatrange
from postgis import Geometry, Point, MultiPoint, LineString, GeometryCollection, MultiLineString
from MobilityDB.TimeTypes import TimestampSet, Period, PeriodSet
from MobilityDB.MainTypes import *
from MobilityDB.BoxTypes import *

ti = TGeomPointInst('Point(10.0 10.0)@2019-09-08 00:00:00+01')
print(ti)

ti = TGeomPointInst(['Point(10.0 10.0)', '2019-09-08 00:00:00+01'])
print(ti)

ti = TGeomPointInst(['Point(10.0 10.0)', parse('2019-09-08 00:00:00+01')])
print(ti)


"""
ti = TBoolI('{True@2019-09-01 00:00:00+01, False@2019-09-02 00:00:00+01, True@2019-09-03 00:00:00+01}')
print(ti)

inst = TBoolInst('True', parse('2000-01-01'))
print(inst)
print(inst.BaseClass)
"""




