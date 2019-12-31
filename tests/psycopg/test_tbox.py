import pytest

from MobilityDB import TBox


@pytest.mark.parametrize('expected_tbox', [
	'TBOX((10.0, 2019-09-08 00:00:00+02), (30.0, 2019-09-10 00:00:00+02))',
	'TBOX((, 2019-09-08 00:00:00+02), (, 2019-09-10 00:00:00+02))',
	'TBOX((10.0, ), (30.0, ))'
])
def test_tbox_constructor(cursor, expected_tbox):
	params = TBox(expected_tbox)
	cursor.execute("INSERT INTO tbl_tbox (box) VALUES (%s)" % params)
	cursor.execute("SELECT box FROM tbl_tbox WHERE box=%s" % params)
	result = cursor.fetchone()[0]
	assert result == TBox(expected_tbox)
