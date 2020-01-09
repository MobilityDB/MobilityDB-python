from mobilitydb import TBox, STBox

print("############################")
print('# Create new TBOX instances')
print("############################")

print('\n# Input string')

# Both value and time dimensions
var = TBox('TBOX((1.0, 2000-01-01), (2.0, 2000-01-02))')
print(var)
# Only value dimension
var = TBox('TBOX((1.0,), (2.0,))')
print(var)
# Only time dimension
var = TBox('TBOX((, 2000-01-01), (, 2000-01-02))')
print(var)

print('\n# Constructors')

# Both value and time dimensions
var = TBox(1.0, '2001-01-01', 2.0, '2001-01-02')
print(var)
# Only value dimension
var = TBox(1.0, 2.0)
print(var)
# Only time dimension
var = TBox('2001-01-01', '2001-01-02')
print(var)

print("\n############################")
print('# Create new STBOX instances')
print("############################")

print('\n# Input string')

# Only coordinate (X and Y) dimension
var = STBox('STBOX((1.0, 2.0), (1.0, 2.0))')
print(var)
# Only coordinate (X, Y and Z) dimension
var = STBox('STBOX Z((1.0, 2.0, 3.0), (1.0, 2.0, 3.0))')
print(var)
# Both coordinate (X, Y) and time dimensions
var = STBox('STBOX T((1.0, 2.0, 2001-01-03), (1.0, 2.0, 2001-01-03))')
print(var)
# Both coordinate (X, Y, and Z) and time dimensions
var = STBox('STBOX ZT((1.0, 2.0, 3.0, 2001-01-04), (1.0, 2.0, 3.0, 2001-01-04))')
print(var)
# Only time dimension
var = STBox('STBOX T(( , , 2001-01-03), ( , , 2001-01-03))')
print(var)
# Only geodetic coordinate (X, Y and Z) dimension
var = STBox('GEODSTBOX((1.0, 2.0, 3.0), (1.0, 2.0, 3.0))')
print(var)
#  Both geodetic coordinate (X, Y, and Z) and time dimensions
var = STBox('GEODSTBOX T((1.0, 2.0, 3.0, 2001-01-04), (1.0, 2.0, 3.0, 2001-01-04))')
print(var)
# Only time dimension for geodetic box
var = STBox('GEODSTBOX T(( , , 2001-01-03), ( , , 2001-01-03))')
print(var)

print('\n# Constructors')

# Only coordinate (X and Y) dimension
var = STBox(1.0, 2.0, 1.0, 2.0)
print(var)
# Only coordinate (X, Y and Z) dimension
var = STBox(1.0, 2.0, 3.0, 1.0, 2.0, 3.0)
print(var)
# Both coordinate (X, Y) and time dimensions
var = STBox(1.0, 2.0, '2001-01-03', 1.0, 2.0, '2001-01-03')
print(var)
# Both coordinate (X, Y, and Z) and time dimensions
var = STBox(1.0, 2.0, 3.0, '2001-01-04', 1.0, 2.0, 3.0, '2001-01-04')
print(var)
# Only time dimension
var = STBox('2001-01-03', '2001-01-03')
print(var)
# Only geodetic coordinate (X, Y and Z) dimension
var = STBox(1.0, 2.0, 3.0, 1.0, 2.0, 3.0, geodetic=True)
print(var)
#  Both geodetic coordinate (X, Y, and Z) and time dimensions
var = STBox(1.0, 2.0, 3.0, '2001-01-04', 1.0, 2.0, 3.0, '2001-01-03', geodetic=True)
print(var)
# Only time dimension for geodetic box
var = STBox('2001-01-03', '2001-01-03', geodetic=True)
print(var)
