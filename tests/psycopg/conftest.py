import pytest
from MobilityDB import *
from tests.psycopg import *

db = psycopg2.connect(host='localhost', dbname="sf0_005", user='postgres', password='ulb')
db.autocommit = True

MobilityDBRegister(db)
cur = db.cursor()


def pytest_configure():
    cur.execute('CREATE TABLE IF NOT EXISTS tbl_tgeompoint (tgeompoint_col tgeompoint NOT NULL)')
    cur.execute('CREATE TABLE IF NOT EXISTS tbl_tint (tint_col tint NOT NULL)')


def pytest_unconfigure():
    cur.execute('DROP TABLE tbl_tgeompoint, tbl_tint')



@pytest.fixture
def cursor():
    # Make sure tables are clean.
    cur.execute('TRUNCATE TABLE tbl_tgeompoint')
    cur.execute('TRUNCATE TABLE tbl_tint')
    return cur
