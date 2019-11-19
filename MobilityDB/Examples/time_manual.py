from MobilityDB import *

print("\n# PERIOD")

# Constructor

var = PERIOD('[2019-09-08, 2019-09-10]')
print("Constructor string:", var)
var = PERIOD('[2019-09-08, 2019-09-10)')
print("Constructor string:", var)
var = PERIOD('(2019-09-08, 2019-09-10]')
print("Constructor string:", var)
var = PERIOD('(2019-09-08, 2019-09-10)')
print("Constructor string:", var)
var = PERIOD('2019-09-08', '2019-09-10')
print("Constructor 2 args:", var)
var = PERIOD('2019-09-08', '2019-09-10', False, True)
print("Constructor 4 args:", var)

# Accessor functions
var1 = var.lower()
print("lower:", var1)
var1 = var.upper()
print("upper:", var1)
var1 = var.lower_inc()
print("lower_inc:", var1)
var1 = var.upper_inc()
print("upper_inc:", var1)

print("\n# TIMESTAMPSET")

# Constructor
var = TIMESTAMPSET('{2019-09-08, 2019-09-10, 2019-09-11, 2019-09-12}')
print("Constructor string:  ", var)
var = TIMESTAMPSET('2019-09-08', '2019-09-10', '2019-09-11', '2019-09-12')
print("Constructor elements:", var)

# Accessor functions
var1 = var.timespan()
print("Timespan:", var1)
var1 = var.numTimestamps()
print("numTimestamps:", var1)
var1 = var.startTimestamp()
print("startTimestamp:", var1)
var1 = var.endTimestamp()
print("endTimestamp:", var1)
var1 = var.timestampN(1)
print("timestampN(1):", var1)
var1 = var.timestampN(4)
print("timestampN(4):", var1)
var1 = var.timestamps()
print("timestamps:", var1)

print("\n# PERIODSET")

# Constructor
var = PERIODSET('{[2019-09-08, 2019-09-10], [2019-09-11, 2019-09-12), (2019-09-13,2019-09-13], (2019-09-14, 2019-09-15]}')
print("Constructor string:  ",var)
var = PERIODSET('[2019-09-08, 2019-09-10]', '[2019-09-11, 2019-09-12)', '(2019-09-13,2019-09-13]', '(2019-09-14, 2019-09-15)')
print("Constructor elements:",var)

