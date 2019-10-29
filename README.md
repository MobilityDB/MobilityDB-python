# MobilityDB-Python
MobilityDB-Python is a python package that is used as an API to access MobilityDB. 

Install
------------
    pip install MobilityDB
    
Requirements
------------
 - Python >= 3.0
 - MobilityDB
 
Usage
------------ 
1- Register MobilityDB extension in PostgreSQL driver:

    from MobilityDB import *
    connectionObject = psycopg2.connect(host='localhost', database='db', user='postgres', password='')
    MobilityDBRegister(connectionObject)

2- Retrieve MobilityDB types as python objects:

    --To get MobilityDB tgeompoint(Sequence) type
    cursor.execute('SELECT tpoint from tpointseq;')
    colVal = cursor.fetchone()[0]
    print(colVal)
    
    --Result is an object of TGEOMPOINTSEQ type:
    --TGEOMPOINT(SEQUENCE)'[POINT(1.0 2.0)@2019-09-08 00:00:00+02:00, POINT(0.0 2.0)@2019-09-09 00:00:00+02:00, POINT(1.0 1.0)@2019-09-10 00:00:00+02:00]'
    
    --Accessor functions
    getValue(ttype)
    getValues(ttype)
    getTimestamp(ttype)
    timespan(ttype)
    startInstant(ttype)
    endInstant(ttype)
    startValue(ttype)
    endValue(ttype)
    instantsN(ttype, n)
    getType(ttype)
    