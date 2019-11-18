from MobilityDB import *

var = PERIOD('[2019-09-08, 2019-09-10]')
print(var)
var = PERIOD('[2019-09-08, 2019-09-10)')
print(var)
var = PERIOD('(2019-09-08, 2019-09-10]')
print(var)
var = PERIOD('(2019-09-08, 2019-09-10)')
print(var)


var = PERIOD('2019-09-08', '2019-09-10')
print(var)
var = PERIOD('2019-09-08', '2019-09-10', False, True)
print(var)

var = TIMESTAMPSET('2019-09-08', '2019-09-10', '2019-09-11', '2019-09-12')
print(var)

var = PERIODSET('[2019-09-08, 2019-09-10]', '[2019-09-11, 2019-09-12)', '(2019-09-13,2019-09-13]', '(2019-09-14, 2019-09-15)')
print(var)
var = PERIODSET('{[2019-09-08, 2019-09-10], [2019-09-11, 2019-09-12), (2019-09-13,2019-09-13], (2019-09-14, 2019-09-15]}')
print(var)

