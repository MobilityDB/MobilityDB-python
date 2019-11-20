import pytest
from MobilityDB import *

db = psycopg2.connect(host='localhost', dbname="sf0_005", user='postgres', password='ulb')
db.autocommit = True

MobilityDBRegister(db)
cur = db.cursor()


def pytest_configure():
	cur.execute('CREATE TABLE IF NOT EXISTS tbl_tgeompoint (tgeompoint_col tgeompoint NOT NULL)')
	cur.execute('CREATE TABLE IF NOT EXISTS tbl_tgeogpoint (tgeogpoint_col tgeogpoint NOT NULL)')
	cur.execute('CREATE TABLE IF NOT EXISTS tbl_tint (tint_col tint NOT NULL)')
	cur.execute('CREATE TABLE IF NOT EXISTS tbl_tfloat (tfloat_col tfloat NOT NULL)')
	cur.execute('CREATE TABLE IF NOT EXISTS tbl_tbool (tbool_col tbool NOT NULL)')
	cur.execute('CREATE TABLE IF NOT EXISTS tbl_ttext (ttext_col ttext NOT NULL)')
	cur.execute('CREATE TABLE IF NOT EXISTS tbl_tbox (tbox_col tbox NOT NULL)')
	cur.execute('CREATE TABLE IF NOT EXISTS tbl_stbox (stbox_col stbox NOT NULL)')


def pytest_unconfigure():
	cur.execute('DROP TABLE tbl_tgeompoint, tbl_tgeogpoint, tbl_tint, tbl_tfloat, tbl_tbool, tbl_ttext, '
				'tbl_tbox, tbl_stbox')


@pytest.fixture
def cursor():
	# Make sure tables are clean.
	cur.execute('TRUNCATE TABLE tbl_tgeompoint')
	cur.execute('TRUNCATE TABLE tbl_tgeogpoint')
	cur.execute('TRUNCATE TABLE tbl_tint')
	cur.execute('TRUNCATE TABLE tbl_tfloat')
	cur.execute('TRUNCATE TABLE tbl_tbool')
	cur.execute('TRUNCATE TABLE tbl_ttext')
	cur.execute('TRUNCATE TABLE tbl_tbox')
	cur.execute('TRUNCATE TABLE tbl_stbox')
	return cur
