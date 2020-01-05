import pytest
from MobilityDB import TBox

pytestmark = pytest.mark.asyncio

@pytest.mark.parametrize('expected_tbox', [
	'TBOX((10.0, 2019-09-08 00:00:00+02), (30.0, 2019-09-10 00:00:00+02))',
	'TBOX((, 2019-09-08 00:00:00+02), (, 2019-09-10 00:00:00+02))',
	'TBOX((10.0, ), (30.0, ))'
])
async def test_tbox_constructor(connection, expected_tbox):
	params = TBox(expected_tbox)
	print('params =',params.__class__)
	await connection.execute("INSERT INTO tbl_tbox (box) VALUES ($1)", params)
	print('after =',params)
	result = await connection.fetchval("SELECT box FROM tbl_tbox WHERE box=$1", params)
	assert result == TBox(expected_tbox)
