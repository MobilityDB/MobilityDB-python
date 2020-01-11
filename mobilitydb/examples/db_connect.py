import asyncpg
import psycopg2
import os
    
_pghost = os.getenv('PGHOST', 'localhost')
_pgdb = os.getenv('PGDATABASE', 'regtests')
_pguser = os.getenv('PGUSER', 'mobilitydb')
_pgpassword = os.getenv('PGPASSWORD', '')

def asyncpg_connect():
    return asyncpg.connect(host=_pghost, database=_pgdb, user=_pguser, password=_pgpassword)

def psycopg_connect():
    return psycopg2.connect(host=_pghost, database=_pgdb, user=_pguser, password=_pgpassword)

