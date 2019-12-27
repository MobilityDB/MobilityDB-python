import pytest
from bdateutil.parser import parse
from MobilityDB import TFloatInst, TFloatI, TFloatSeq, TFloatS


@pytest.mark.parametrize('expected_tfloatinst', [
    '10.0@2019-09-01 00:00:00+01',
    ('10.0', '2019-09-08 00:00:00+01'),
    (10.0, parse('2019-09-08 00:00:00+01')),
])
def test_tfloatinst_should_round(cursor, expected_tfloatinst):
    params = [TFloatInst(expected_tfloatinst)]
    cursor.execute('INSERT INTO tbl_tfloatinst (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tfloatinst WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    assert result == TFloatInst(expected_tfloatinst)

@pytest.mark.parametrize('expected_tfloati', [
    '{10.0@2019-09-01 00:00:00+01, 20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01}',
    #('10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'),
    # (TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'), TFloatInst('10.0@2019-09-03 00:00:00+01')),
    ['10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'],
    [TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'), TFloatInst('10.0@2019-09-03 00:00:00+01')],
])
def test_tfloati_should_round(cursor, expected_tfloati):
    params = [TFloatI(expected_tfloati)]
    cursor.execute('INSERT INTO tbl_tfloati (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tfloati WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    assert result == TFloatI(expected_tfloati)

@pytest.mark.parametrize('expected_tfloatseq', [
    '[10.0@2019-09-01 00:00:00+01, 20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]',
    #('10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'),
    # (TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'), TFloatInst('10.0@2019-09-03 00:00:00+01')),
    ['10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'],
    [TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'), TFloatInst('10.0@2019-09-03 00:00:00+01')],
])
def test_tfloatseq_should_round(cursor, expected_tfloatseq):
    params = [TFloatSeq(expected_tfloatseq)]
    cursor.execute('INSERT INTO tbl_tfloatseq (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tfloatseq WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    assert result == TFloatSeq(expected_tfloatseq)

@pytest.mark.parametrize('expected_tfloats', [
    '{[10.0@2019-09-01 00:00:00+01], [20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]}',
    #('10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'),
    # (TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'), TFloatInst('10.0@2019-09-03 00:00:00+01')),
    ['[10.0@2019-09-01 00:00:00+01]', '[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]'],
    [TFloatSeq('[10.0@2019-09-01 00:00:00+01]'), TFloatSeq('[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]')],
])
def test_tfloats_should_round(cursor, expected_tfloats):
    params = [TFloatS(expected_tfloats)]
    cursor.execute('INSERT INTO tbl_tfloats (temp) VALUES (%s)', params)
    cursor.execute('SELECT temp FROM tbl_tfloats WHERE temp=%s', params)
    result = cursor.fetchone()[0]
    assert result == TFloatS(expected_tfloats)


