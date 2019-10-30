import pytest

from MobilityDB import TINT


@pytest.mark.parametrize('expected', [
    ('10@2019-09-01'),
     ('{8@2019-08-03, 13@2019-08-05, 10@2019-09-01}'),
     ('[8@2019-08-03, 13@2019-08-05, 10@2019-09-01]'),
     ('{[8@2019-08-03, 13@2019-08-05, 10@2019-09-01],[20@2019-09-03]}'),
])
def test_tint_should_round(cursor, expected):
    params = [TINT(expected)]
    cursor.execute('INSERT INTO tbl_tint (tint_col) VALUES (%s)', params)
    cursor.execute('SELECT tint_col FROM tbl_tint WHERE tint_col=%s', params)
    result = cursor.fetchone()[0]
    assert result == TINT(expected)
