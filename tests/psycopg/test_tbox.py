import pytest
from dateutil.parser import parse
from mobilitydb import TBox


@pytest.mark.parametrize('expected_tbox', [
	'TBOX((10.0, 2019-09-08 00:00:00+02), (30.0, 2019-09-10 00:00:00+02))',
	'TBOX((, 2019-09-08 00:00:00+02), (, 2019-09-10 00:00:00+02))',
	'TBOX((10.0, ), (30.0, ))',
	('10.0', '20.0'),
	(10.0, 20.0),
	('2019-09-08 00:00:00+01', '2019-09-08 00:00:00+01'),
	(parse('2019-09-08 00:00:00+01'), parse('2019-09-08 00:00:00+01')),
	('10.0', '2019-09-08 00:00:00+01', '20.0', '2019-09-08 00:00:00+01'),
	(10.0, parse('2019-09-08 00:00:00+01'), 20.0, parse('2019-09-08 00:00:00+01')),
])
def test_tbox_constructor(cursor, expected_tbox):
	if isinstance(expected_tbox, tuple):
		params = TBox(*expected_tbox)
	else:
		params = TBox(expected_tbox)
	cursor.execute("INSERT INTO tbl_tbox (box) VALUES (%s)" % params)
	cursor.execute("SELECT box FROM tbl_tbox WHERE box=%s" % params)
	result = cursor.fetchone()[0]
	if isinstance(expected_tbox, tuple):
		assert result == TBox(*expected_tbox)
	else:
		assert result == TBox(expected_tbox)
