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
   
   1.  Functions and Operators for Time Types and Range Types
    
    1.1 Constructor Functions
        period(timestamptz, timestamptz, boolean = true, boolean = false):  period
        timestampset(timestamptz[]}):  timestampset
        
    1.3  Accessor Functions
        lower(period):  timestamptz
        upper(period):  timestamptz
    