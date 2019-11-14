import pytest

from MobilityDB import TBOOL


@pytest.mark.parametrize('expected', [
    ('false@2019-09-01'),
     ('{true@2019-08-03, true@2019-08-05, false@2019-09-01}'),
     ('[true@2019-08-03, true@2019-08-05, false@2019-09-01]'),
     ('{[true@2019-08-03, true@2019-08-05, false@2019-09-01],[false@2019-09-03]}'),
])
def test_tint_should_round(cursor, expected):
    params = [TBOOL(expected)]
    cursor.execute('INSERT INTO tbl_tbool (tbool_col) VALUES (%s)', params)
    cursor.execute('SELECT tbool_col FROM tbl_tbool WHERE tbool_col=%s', params)
    result = cursor.fetchone()[0]
    assert result == TBOOL(expected)
