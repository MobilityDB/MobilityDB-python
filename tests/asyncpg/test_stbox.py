import pytest
from dateutil.parser import parse
from mobilitydb import STBox

pytestmark = pytest.mark.asyncio

@pytest.mark.parametrize('expected_stbox', [
	# Only coordinate (X and Y) dimension
	'STBOX ((1.0, 2.0), (1.0, 2.0))',
	('1.0', '2.0', '3.0', '4.0'),
	(1.0, 2.0, 3.0, 4.0),
	# Only coordinate (X, Y and Z) dimension
	'STBOX Z((1.0, 2.0, 3.0), (1.0, 2.0, 3.0))',
	('1.0', '2.0', '3.0', '4.0', '5.0', '6.0'),
	(1.0, 2.0, 3.0, 4.0, 5.0, 6.0),
	# Both coordinate (X, Y) and time dimensions
	'STBOX T((1.0, 2.0, 2001-01-03 00:00:00+01), (1.0, 2.0, 2001-01-03 00:00:00+01))',
	(1.0, 2.0, '2001-01-01 00:00:00+01', 3.0, 4.0, '2001-01-02 00:00:00+01'),
	(1.0, 2.0, parse('2001-01-01 00:00:00+01'), 3.0, 4.0, parse('2001-01-02 00:00:00+01')),
	# Both coordinate (X, Y, and Z) and time dimensions
	'STBOX ZT((1.0, 2.0, 3.0, 2001-01-04 00:00:00+01), (1.0, 2.0, 3.0, 2001-01-04 00:00:00+01))',
	(1.0, 2.0, 3.0, '2001-01-01 00:00:00+01', 4.0, 5.0, 6.0, '2001-01-02 00:00:00+01'),
	(1.0, 2.0, 3.0, parse('2001-01-01 00:00:00+01'), 4.0, 5.0, 6.0, parse('2001-01-02 00:00:00+01')),
	# Only time dimension
	'STBOX T(, 2001-01-03 00:00:00+01), (, 2001-01-03 00:00:00+01))',
	('2001-01-03 00:00:00+01', '2001-01-03 00:00:00+01'),
	(parse('2001-01-03 00:00:00+01'), parse('2001-01-03 00:00:00+01')),
	# Only geodetic coordinate (X, Y and Z) dimension
	'GEODSTBOX((1.0, 2.0, 3.0), (1.0, 2.0, 3.0))',
	# (1.0, 2.0, 3.0, 4.0, 5.0, 6.0, True),
	#  Both geodetic coordinate (X, Y, and Z) and time dimensions
	'GEODSTBOX T((1.0, 2.0, 3.0, 2001-01-03 00:00:00+01), (1.0, 2.0, 3.0, 2001-01-04 00:00:00+01))',
	# (1.0, 2.0, 3.0, '2001-01-01 00:00:00+01', 4.0, 5.0, 6.0, '2001-01-02 00:00:00+01', True),
	# Only time dimension for geodetic box
	'GEODSTBOX T((, 2001-01-03 00:00:00+01), (, 2001-01-03 00:00:00+01))',
	# ('2001-01-01 00:00:00+01', '2001-01-02 00:00:00+01', True),
])
async def test_stbox_constructor(connection, expected_stbox):
	if isinstance(expected_stbox, tuple):
		params = STBox(*expected_stbox)
	else:
		params = STBox(expected_stbox)
	print(params.__class__)
	print(params.xmax())
	await connection.execute("INSERT INTO tbl_stbox (box) VALUES ($1)", params)
	result = await connection.fetchval("SELECT box FROM tbl_stbox WHERE box=$1", params, column=0)
	if isinstance(expected_stbox, tuple):
		assert result == STBox(*expected_stbox)
	else:
		assert result == STBox(expected_stbox)
