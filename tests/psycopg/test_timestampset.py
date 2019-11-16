import pytest

from MobilityDB import TIMESTAMPSET


@pytest.mark.parametrize('expected', [
    ('2019-09-08', '2019-09-10', '2019-09-11')
])
def test_tint_should_round(cursor, expected):
    params = TIMESTAMPSET(expected)
    cursor.execute("INSERT INTO tbl_timestampset (timestampset_col) VALUES ('%s')" % params)
    cursor.execute("SELECT timestampset_col FROM tbl_timestampset WHERE timestampset_col='%s'" % params)
    result = cursor.fetchone()[0]
    # assert result == TIMESTAMPSET(expected)
