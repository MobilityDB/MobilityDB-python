import pytest

from MobilityDB import TFLOAT


@pytest.mark.parametrize('expected', [
    ('10.0@2019-09-01'),
     ('{8.0@2019-08-03, 13.0@2019-08-05, 10.0@2019-09-01}'),
     ('[8.0@2019-08-03, 13.0@2019-08-05, 10.0@2019-09-01]'),
     ('{[8.0@2019-08-03, 13.0@2019-08-05, 10.0@2019-09-01],[20.0@2019-09-03]}'),
])
def test_tint_should_round(cursor, expected):
    params = [TFLOAT(expected)]
    cursor.execute('INSERT INTO tbl_tfloat (tfloat_col) VALUES (%s)', params)
    cursor.execute('SELECT tfloat_col FROM tbl_tfloat WHERE tfloat_col=%s', params)
    result = cursor.fetchone()[0]
    assert result == TFLOAT(expected)
