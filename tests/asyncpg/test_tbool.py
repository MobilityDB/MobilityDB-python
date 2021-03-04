###############################################################################
#
# This MobilityDB code is provided under The PostgreSQL License.
#
# Copyright (c) 2019-2021, Université libre de Bruxelles and MobilityDB
# contributors
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose, without fee, and without a written 
# agreement is hereby granted, provided that the above copyright notice and
# this paragraph and the following two paragraphs appear in all copies.
#
# IN NO EVENT SHALL UNIVERSITE LIBRE DE BRUXELLES BE LIABLE TO ANY PARTY FOR
# DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING
# LOST PROFITS, ARISING OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION,
# EVEN IF UNIVERSITE LIBRE DE BRUXELLES HAS BEEN ADVISED OF THE POSSIBILITY 
# OF SUCH DAMAGE.
#
# UNIVERSITE LIBRE DE BRUXELLES SPECIFICALLY DISCLAIMS ANY WARRANTIES, 
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS FOR A PARTICULAR PURPOSE. THE SOFTWARE PROVIDED HEREUNDER IS ON
# AN "AS IS" BASIS, AND UNIVERSITE LIBRE DE BRUXELLES HAS NO OBLIGATIONS TO 
# PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS. 
#
###############################################################################

import pytest
from dateutil.parser import parse
from mobilitydb.main import TBoolInst, TBoolInstSet, TBoolSeq, TBoolSeqSet

pytestmark = pytest.mark.asyncio

@pytest.mark.parametrize('expected_tboolinst', [
    'true@2019-09-01 00:00:00+01',
    ('true', '2019-09-08 00:00:00+01'),
    ['true', '2019-09-08 00:00:00+01'],
    (True, '2019-09-08 00:00:00+01'),
    [True, parse('2019-09-08 00:00:00+01')],
])
async def test_tboolinst_constructors(connection, expected_tboolinst):
    params = TBoolInst(expected_tboolinst)
    await connection.execute('INSERT INTO tbl_tboolinst (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tboolinst WHERE temp=$1', params, column=0)
    assert result == TBoolInst(expected_tboolinst)

@pytest.mark.parametrize('expected_tboolinstset', [
    '{true@2019-09-01 00:00:00+01, false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01}',
    ('true@2019-09-01 00:00:00+01', 'false@2019-09-02 00:00:00+01', 'true@2019-09-03 00:00:00+01'),
    (TBoolInst('true@2019-09-01 00:00:00+01'), TBoolInst('false@2019-09-02 00:00:00+01'),
     TBoolInst('true@2019-09-03 00:00:00+01')),
    ['true@2019-09-01 00:00:00+01', 'false@2019-09-02 00:00:00+01', 'true@2019-09-03 00:00:00+01'],
    [TBoolInst('true@2019-09-01 00:00:00+01'), TBoolInst('false@2019-09-02 00:00:00+01'),
     TBoolInst('true@2019-09-03 00:00:00+01')],
])
async def test_tboolinstset_constructor(connection, expected_tboolinstset):
    if isinstance(expected_tboolinstset, tuple):
        params = TBoolInstSet(*expected_tboolinstset)
    else:
        params = TBoolInstSet(expected_tboolinstset)
    await connection.execute('INSERT INTO tbl_tboolinstset (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tboolinstset WHERE temp=$1', params)
    if isinstance(expected_tboolinstset, tuple):
        assert result == TBoolInstSet(*expected_tboolinstset)
    else:
        assert result == TBoolInstSet(expected_tboolinstset)

@pytest.mark.parametrize('expected_tboolseq', [
    '[true@2019-09-01 00:00:00+01, false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]',
    ['true@2019-09-01 00:00:00+01', 'false@2019-09-02 00:00:00+01', 'false@2019-09-03 00:00:00+01'],
    [TBoolInst('true@2019-09-01 00:00:00+01'), TBoolInst('false@2019-09-02 00:00:00+01'),
     TBoolInst('false@2019-09-03 00:00:00+01')],
])
async def test_tboolseq_constructor(connection, expected_tboolseq):
    if isinstance(expected_tboolseq, tuple):
        params = TBoolSeq(*expected_tboolseq)
    else:
        params = TBoolSeq(expected_tboolseq)
    await connection.execute('INSERT INTO tbl_tboolseq (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tboolseq WHERE temp=$1', params)
    if isinstance(expected_tboolseq, tuple):
        assert result == TBoolSeq(*expected_tboolseq)
    else:
        assert result == TBoolSeq(expected_tboolseq)

@pytest.mark.parametrize('expected_tboolseqset', [
    '{[true@2019-09-01 00:00:00+01], [false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]}',
    ['[true@2019-09-01 00:00:00+01]', '[false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]'],
    [TBoolSeq('[true@2019-09-01 00:00:00+01]'),
     TBoolSeq('[false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]')],
])
async def test_tboolseqset_constructor(connection, expected_tboolseqset):
    if isinstance(expected_tboolseqset, tuple):
        params = TBoolSeqSet(*expected_tboolseqset)
    else:
        params = TBoolSeqSet(expected_tboolseqset)
    await connection.execute('INSERT INTO tbl_tboolseqset (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tboolseqset WHERE temp=$1', params)
    if isinstance(expected_tboolseqset, tuple):
        assert result == TBoolSeqSet(*expected_tboolseqset)
    else:
        assert result == TBoolSeqSet(expected_tboolseqset)
