from datetime import datetime, timedelta
from dateutil.parser import parse
from mobilitydb.time import TimestampSet, Period, PeriodSet

print("\n# Period")

# Constructors
var = Period('[2019-09-08, 2019-09-10]')
print("Constructor string:", var)
var = Period('[2019-09-08, 2019-09-10)')
print("Constructor string:", var)
var = Period('(2019-09-08, 2019-09-10]')
print("Constructor string:", var)
var = Period('(2019-09-08, 2019-09-10)')
print("Constructor string:", var)
var = Period('2019-09-08', '2019-09-10')
print("Constructor 2 args:", var)
var = Period('2019-09-08', '2019-09-10', False, True)
print("Constructor 4 args:", var)

# Accessor functions
var1 = var.lower
print("lower:", var1)
var1 = var.upper
print("upper:", var1)
var1 = var.lower_inc
print("lower_inc:", var1)
var1 = var.upper_inc
print("upper_inc:", var1)
var1 = var.timespan
print("timespan:", var1)
var1 = var.shift(timedelta(days=1))
print("shift:", var1)

# Comparisons
var1 = Period('2019-09-08', '2019-09-10', True, True)
var2 = Period('2019-09-08', '2019-09-10', False, True)
print("Eq:", var1 == var2)
print("Lt:", var1 < var2)
print("Le:", var1 <= var2)
print("Gt:", var1 > var2)
print("Ge:", var1 >= var2)

print("\n# TimestampSet")

# Constructor with a single argument of type string
var = TimestampSet('{2019-09-08, 2019-09-10, 2019-09-11, 2019-09-12}')
print("Constructor string:   ", var)
# Constructor with multiple arguments of type string
var = TimestampSet('2019-09-08', '2019-09-10', '2019-09-11', '2019-09-12')
print("Constructor strings:  ", var)
# Constructor with multiple arguments of type datetime
t1 = datetime.strptime('2019-09-08', '%Y-%m-%d')
t2 = datetime.strptime('2019-09-10', '%Y-%m-%d')
t3 = datetime.strptime('2019-09-11', '%Y-%m-%d')
t4 = datetime.strptime('2019-09-12', '%Y-%m-%d')
var = TimestampSet(t1, t2, t3, t4)
print("Constructor datetimes:", var)
# Constructor with a single argument of type list of strings
var = TimestampSet(['2019-09-08', '2019-09-10', '2019-09-11', '2019-09-12'])
print("Constructor list of strings:  ", var)
# Constructor with a single argument of type list of periods
var = TimestampSet([t1, t2, t3, t4])
print("Constructor list of datetimes:", var)

# Error
# t4 = datetime.strptime('2019-09-11', '%Y-%m-%d')
# var = TimestampSet(t1, t2, t3, t4)

# Accessor functions
var1 = var.period
print("period:", var1)
var1 = var.numTimestamps
print("numTimestamps:", var1)
var1 = var.startTimestamp
print("startTimestamp:", var1)
var1 = var.endTimestamp
print("endTimestamp:", var1)
var1 = var.timestampN(1)
print("timestampN(1):", var1)
var1 = var.timestampN(4)
print("timestampN(4):", var1)
var1 = var.timestamps
print("timestamps:", var1)
var1 = var.shift(timedelta(days=1))
print("shift:", var1)

print("\n# PeriodSet")

# Constructor with a single argument of type string
var = PeriodSet('{[2019-09-08, 2019-09-10], [2019-09-11, 2019-09-12), \
    [2019-09-13,2019-09-13], (2019-09-14, 2019-09-15]}')
print("Constructor string: ", var)
# Constructor with multiple arguments of type string
var = PeriodSet('[2019-09-08, 2019-09-10]', '[2019-09-11, 2019-09-12)', \
                '[2019-09-13,2019-09-13]', '(2019-09-14, 2019-09-15)')
print("Constructor strings:", var)
# Constructor with multiple arguments of type period
p1 = Period('[2019-09-08, 2019-09-10]')
p2 = Period('[2019-09-11, 2019-09-12)')
p3 = Period('[2019-09-13,2019-09-13]')
p4 = Period('(2019-09-14, 2019-09-15)')
var = PeriodSet(p1, p2, p3, p4)
print("Constructor periods:", var)
# Constructor with a single argument of type list of strings
var = PeriodSet(['[2019-09-08, 2019-09-10]', '[2019-09-11, 2019-09-12)', \
                 '[2019-09-13,2019-09-13]', '(2019-09-14, 2019-09-15)'])
print("Constructor list of strings:", var)
# Constructor with a single argument of type list of periods
var = PeriodSet([p1, p2, p3, p4])
print("Constructor list of periods:", var)

# Error
# t4 = datetime.strptime('2019-09-11', '%Y-%m-%d')
# var = PeriodSet(p1, p2, p3, p4)

# Accessor functions
var1 = var.timespan
print("timespan:", var1)
var1 = var.period
print("period:", var1)
var1 = var.numTimestamps
print("numTimestamps:", var1)
var1 = var.startTimestamp
print("startTimestamp:", var1)
var1 = var.endTimestamp
print("endTimestamp:", var1)
var1 = var.timestampN(1)
print("timestampN(1):", var1)
var1 = var.timestamps
print("timestamps:", var1)

var1 = var.numPeriods
print("numPeriods:", var1)
var1 = var.startPeriod
print("startPeriod:", var1)
var1 = var.endPeriod
print("endPeriod:", var1)
var1 = var.periodN(1)
print("periodN(1):", var1)
var1 = var.periods
print("periods:", var1)
var1 = var.shift(timedelta(days=1))
print("shift:", var1)

p1 = Period('[2019-09-08, 2019-09-10]')
p2 = Period('[2019-09-11, 2019-09-12)')
print ("overlap:", p1.overlap(p2))
p2 = Period('[2019-09-09, 2019-09-12)')
print ("overlap:", p1.overlap(p2))

p1 = Period('[2019-09-08, 2019-09-10]')
p2 = Period('[2019-09-08, 2019-09-10]')
p3 = Period('[2019-09-11, 2019-09-12)')
print ("Period equality:", p1 == p2)
print ("Period equality:", p1 == p3)

ts1 = TimestampSet('{2019-09-08, 2019-09-10}')
ts2 = TimestampSet('{2019-09-08, 2019-09-10}')
ts3 = TimestampSet('{2019-09-08, 2019-09-10, 2019-09-11}')
print ("TimestampSet equality:", ts1 == ts2)
print ("TimestampSet equality:", ts1 == ts3)

ps1 = PeriodSet('{[2019-09-08, 2019-09-10],[2019-09-11, 2019-09-12)}')
ps2 = PeriodSet('{[2019-09-08, 2019-09-10],[2019-09-11, 2019-09-12)}')
ps3 = PeriodSet('{[2019-09-08, 2019-09-10],[2019-09-11, 2019-09-12]}')
ps4 = PeriodSet('{[2019-09-11, 2019-09-12)}')
print ("PeriodSet equality:", ps1 == ps2)
print ("PeriodSet equality:", ps1 == ps3)
print ("PeriodSet equality:", ps1 == ps4)

print ("Time types equality:", p1 == ts1)
print ("Time types equality:", p1 == ps1)
print ("Time types equality:", ts1 == ps1)

print("representantion:", repr(p1))
print("representantion:", repr(ts1))
print("representantion:", repr(ps1))


