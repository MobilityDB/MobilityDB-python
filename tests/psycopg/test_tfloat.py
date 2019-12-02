import pytest
from bdateutil.parser import parse
from MobilityDB import TFloatInst


@pytest.mark.parametrize('expected_tfloatInst', [
    '10.0@2019-09-01',
    ('10.0', '2019-09-08'),
    (10.0, parse('2019-09-08')),
])
def test_tfloatinst_should_round(cursor, expected_tfloatInst):
    params = [TFloatInst(expected_tfloatInst)]
    cursor.execute('INSERT INTO tbl_TFloatInst (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_TFloatInst WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    assert result == TFloatInst(expected_tfloatInst)

