"""
import pytest
from MobilityDB import TTEXT


@pytest.mark.parametrize('expected', [
	'text1@2019-09-01',
	'{text1@2019-08-03, text2@2019-08-05, text3@2019-09-01}',
	'[text1@2019-08-03, text2@2019-08-05, text3@2019-09-01]',
	'{[text1@2019-08-03, text2@2019-08-05, text3@2019-09-01],[text4@2019-09-03]}',
])
def test_ttext_should_round(cursor, expected):
	params = TTEXT(expected)
	cursor.execute('INSERT INTO tbl_ttext (ttext_col) VALUES (%s)' % params)
	cursor.execute('SELECT ttext_col FROM tbl_ttext WHERE ttext_col=%s' % params)
	result = cursor.fetchone()[0]
	assert result == TTEXT(expected)
"""