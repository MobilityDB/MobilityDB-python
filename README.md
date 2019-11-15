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
    --TGEOMPOINT '[POINT(1.0 2.0)@2019-09-08 00:00:00+02:00, POINT(0.0 2.0)@2019-09-09 00:00:00+02:00, POINT(1.0 1.0)@2019-09-10 00:00:00+02:00]'
   
   1  Functions and Operators for Time Types and Range Types
    
    1.1 Constructor Functions
            period(timestamptz, timestamptz, boolean = true, boolean = false):  period
            timestampset(timestamptz[]}):  timestampset
        
    1.3  Accessor Functions
            lower(period):  timestamptz
            upper(period):  timestamptz
            lower_inc(period):  boolean
            upper_inc(period):  boolean
            numPeriods(periodset):  int
            startPeriod(periodset):  period
            endPeriod(periodset):  period
            periodN(periodset, int):  period
            periods(periodset):  period[]
        
  2  Functions and Operators for Temporal Types
    
    2.1  Constructor Functions
            Constructors for tbox
                tbox(float, float):  tbox
                tboxt(timestamptz, timestamptz):  tbox
                tbox(float, timestamptz, float, timestamptz):  tbox
            Constructors for stbox
                stbox(float, float, float, float):  stbox
                stbox(float, float, float, float, float, float):  stbox
                stboxt(float, float, timestamptz, float, float, timestamptz):  stbox
                stbox(float, float, float, timestamptz, float, float, float, timestamptz):  stbox
                geodstbox(float, float, float, float, float, float):  stbox
                geodstbox(float, float, float, timestamptz, float, float, float, timestamptz):  stbox
                stbox(timestamptz, timestamptz):  stbox
    2.4  Accessor Functions
            getType(ttype):  {’Instant’, ’InstantSet’, ’Sequence’, ’SequenceSet’}
            getValue(ttypeinst):  base
            getValues(ttype):  {base[], floatrange[], geo}
            timespan(ttype):  period
            startValue(ttype):  base
            endValue(ttype):  base
            numInstants(ttype):  int
            startInstant(ttype):  ttypeinst
            endInstant(ttype):  ttypeinst
            instantN(ttype, int):  ttypeinst

    2.8  Comparison Operators
            

            
            
        