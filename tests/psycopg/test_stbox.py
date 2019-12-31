"""
import pytest

from MobilityDB import STBox


@pytest.mark.parametrize('expected', [
	'STBOX ZT((10.0, 50, 100, 2019-09-08 00:00:00+02), (30.0, 60, 200, 2019-09-10 00:00:00+02))',
	'STBOX T((10.0, 50, 2019-09-08 00:00:00+02), (30.0, 60, 2019-09-10 00:00:00+02))',
	'STBOX Z((10.0, 50, 100), (30.0, 60, 200))',
	'STBOX ((10.0, 50), (30.0, 60))',
	'GEODSTBOX T((10, 50, 100,2019-09-08 00:00:00+02), (20, 60, 200, 2019-09-10 00:00:00+02))',
	'GEODSTBOX ((10, 50, 100), (20, 60, 200))'
])
def test_stbox_constructor(cursor, expected):
	params = STBOX(expected)
	cursor.execute("INSERT INTO tbl_stbox (stbox_col) VALUES ('%s')" % params)
	cursor.execute("SELECT stbox_col FROM tbl_stbox WHERE stbox_col='%s'" % params)
	result = cursor.fetchone()[0]

# assert result == STBOX(expected)
"""