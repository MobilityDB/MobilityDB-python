import pytest
from dateutil.parser import parse
from mobilitydb import TBox

pytestmark = pytest.mark.asyncio

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
async def test_tbox_constructor(connection, expected_tbox):
    if isinstance(expected_tbox, tuple):
        params = TBox(*expected_tbox)
    else:
        params = TBox(expected_tbox)
    print('params =',params.__class__)
    await connection.execute("INSERT INTO tbl_tbox (box) VALUES ($1)", params)
    print('after =',params)
    result = await connection.fetchval("SELECT box FROM tbl_tbox WHERE box=$1", params)
    if isinstance(expected_tbox, tuple):
        assert result == TBox(*expected_tbox)
    else:
        assert result == TBox(expected_tbox)
