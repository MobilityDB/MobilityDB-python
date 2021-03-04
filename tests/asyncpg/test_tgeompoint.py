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
from postgis import Point
from mobilitydb.main import TGeomPointInst, TGeomPointInstSet, TGeomPointSeq, TGeomPointSeqSet

pytestmark = pytest.mark.asyncio

@pytest.mark.parametrize('expected_tgeompointinst', [
    'POINT(10.0 10.0)@2019-09-01 00:00:00+01',
    'SRID=4326;POINT(10.0 10.0)@2019-09-01 00:00:00+01',
    ('POINT(10.0 10.0)', '2019-09-08 00:00:00+01'),
    ['POINT(10.0 10.0)', '2019-09-08 00:00:00+01'],
    ('SRID=4326;POINT(10.0 10.0)', '2019-09-08 00:00:00+01'),
    ['SRID=4326;POINT(10.0 10.0)', '2019-09-08 00:00:00+01'],
    (Point(10.0, 10.0), parse('2019-09-08 00:00:00+01')),
    [Point(10.0, 10.0), parse('2019-09-08 00:00:00+01')],
    (Point(10.0, 10.0, srid=4326), parse('2019-09-08 00:00:00+01')),
    [Point(10.0, 10.0, srid=4326), parse('2019-09-08 00:00:00+01')],
])
async def test_tgeompointinst_constructors(connection, expected_tgeompointinst):
    params = TGeomPointInst(expected_tgeompointinst)
    await connection.execute('INSERT INTO tbl_tgeompointinst (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tgeompointinst WHERE temp=$1', params, column=0)
    assert result == TGeomPointInst(expected_tgeompointinst)

@pytest.mark.parametrize('expected_tgeompointinstset', [
    '{Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
        'Point(10.0 10.0)@2019-09-03 00:00:00+01}',
    'SRID=4326;{Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
        'Point(10.0 10.0)@2019-09-03 00:00:00+01}',
    ('Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'),
    ['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'],
    ('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01', 'SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01'),
    ['SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01', 'SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01'],
    (TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')),
    [TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')],
    (TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')),
    [TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')],
])
async def test_tgeompointinstset_constructor(connection, expected_tgeompointinstset):
    if isinstance(expected_tgeompointinstset, tuple):
        params = TGeomPointInstSet(*expected_tgeompointinstset)
    else:
        params = TGeomPointInstSet(expected_tgeompointinstset)
    await connection.execute('INSERT INTO tbl_tgeompointinstset (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tgeompointinstset WHERE temp=$1', params)
    if isinstance(expected_tgeompointinstset, tuple):
        assert result == TGeomPointInstSet(*expected_tgeompointinstset)
    else:
        assert result == TGeomPointInstSet(expected_tgeompointinstset)

@pytest.mark.parametrize('expected_tgeompointseq', [
    '[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
        'Point(10.0 10.0)@2019-09-03 00:00:00+01]',
    'SRID=4326;[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
        'Point(10.0 10.0)@2019-09-03 00:00:00+01]',
    'Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
        'Point(10.0 10.0)@2019-09-03 00:00:00+01]',
    'SRID=4326;Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, '
        'Point(10.0 10.0)@2019-09-03 00:00:00+01]',
    ['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'],
    ['SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01', 'SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01'],
    [TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')],
    [TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')],
    (['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'], True, True, 'Stepwise'),
    (['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'], True, True, 'Linear', 4326),
    (['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01',
        'Point(10.0 10.0)@2019-09-03 00:00:00+01'], True, True, 'Stepwise', 4326),
    ([TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')], True, True, 'Stepwise'),
    ([TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-01 00:00:00+01'),
        TGeomPointInst('SRID=4326;Point(20.0 20.0)@2019-09-02 00:00:00+01'),
        TGeomPointInst('SRID=4326;Point(10.0 10.0)@2019-09-03 00:00:00+01')], True, True, 'Stepwise'),
])
async def test_tgeompointseq_constructor(connection, expected_tgeompointseq):
    if isinstance(expected_tgeompointseq, tuple):
        params = TGeomPointSeq(*expected_tgeompointseq)
    else:
        params = TGeomPointSeq(expected_tgeompointseq)
    await connection.execute('INSERT INTO tbl_tgeompointseq (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tgeompointseq WHERE temp=$1', params)
    if isinstance(expected_tgeompointseq, tuple):
        assert result == TGeomPointSeq(*expected_tgeompointseq)
    else:
        assert result == TGeomPointSeq(expected_tgeompointseq)

@pytest.mark.parametrize('expected_tgeompointseqset', [
    '{[Point(10.0 10.0)@2019-09-01 00:00:00+01], '
        '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]}',
    'SRID=4326;{[Point(10.0 10.0)@2019-09-01 00:00:00+01], '
        '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]}',
    'Interp=Stepwise;{[Point(10.0 10.0)@2019-09-01 00:00:00+01], '
        '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]}',
    'SRID=4326;Interp=Stepwise;{[Point(10.0 10.0)@2019-09-01 00:00:00+01], '
        '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]}',
    ['[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'],
    ['SRID=4326;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        'SRID=4326;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'],
    (['[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'], 'Linear'),
    (['[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'], 'Linear', 4326),
    (['SRID=4326;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        'SRID=4326;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'], 'Linear'),
    (['SRID=4326;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        'SRID=4326;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'], 'Linear', 4326),
    (['Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        'Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'],
        'Stepwise'),
    (['SRID=4326;Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        'SRID=4326;Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'],
        'Stepwise', 4326),
    (['Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]',
        'Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'],
        'Stepwise', 4326),
    [TGeomPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeomPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')],
    ([TGeomPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeomPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')], 'Linear'),
    ([TGeomPointSeq('Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),
        TGeomPointSeq(
            'Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')],
     'Stepwise'),
])
async def test_tgeompointseqset_constructor(connection, expected_tgeompointseqset):
    if isinstance(expected_tgeompointseqset, tuple):
        params = TGeomPointSeqSet(*expected_tgeompointseqset)
    else:
        params = TGeomPointSeqSet(expected_tgeompointseqset)
    await connection.execute('INSERT INTO tbl_tgeompointseqset (temp) VALUES ($1)', params)
    result = await connection.fetchval('SELECT temp FROM tbl_tgeompointseqset WHERE temp=$1', params)
    if isinstance(expected_tgeompointseqset, tuple):
        assert result == TGeomPointSeqSet(*expected_tgeompointseqset)
    else:
        assert result == TGeomPointSeqSet(expected_tgeompointseqset)
