import pytest
from MobilityDB import *

db = psycopg2.connect(host='localhost', dbname="mobilitydb", user='mobilitydb', password='')
db.autocommit = True

MobilityDBRegister(db)
cur = db.cursor()

tfloat_types = [TFloatInst, TFloatI, TFloatSeq, TFloatS]
temporal_types = ['INSTANT', 'INSTANTSET', 'SEQUENCE', 'SEQUENCESET']


def pytest_configure():
    i = 0
    while i < 4:
        cur.execute(
            'CREATE TABLE IF NOT EXISTS tbl_' + tfloat_types[i].__name__.lower() +
            ' (temp TFLOAT(' + temporal_types[i] + ') NOT NULL);')
        i += 1


def pytest_unconfigure():
    pass
    # for tfloat_type in tfloat_types:
        # cur.execute('DROP TABLE tbl_' + tfloat_type.__name__)


@pytest.fixture
def cursor():
    # Make sure tables are clean.
    for tfloat_type in tfloat_types:
        cur.execute('TRUNCATE TABLE tbl_' + tfloat_type.__name__)
    return cur
