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
from mobilitydb import TimestampSet, Period, PeriodSet

pytestmark = pytest.mark.asyncio

@pytest.mark.parametrize('expected_timestampset', [
    '{2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01, 2019-09-11 00:00:00+01}',
    ['2019-09-08 00:00:00+01', '2019-09-10 00:00:00+01', '2019-09-11 00:00:00+01'],
    [parse('2019-09-08 00:00:00+01'), parse('2019-09-10 00:00:00+01'), parse('2019-09-11 00:00:00+01')],
    ('2019-09-08 00:00:00+01', '2019-09-10 00:00:00+01', '2019-09-11 00:00:00+01'),
    (parse('2019-09-08 00:00:00+01'), parse('2019-09-10 00:00:00+01'), parse('2019-09-11 00:00:00+01')),
])
async def test_timestampset_constructor(connection, expected_timestampset):
    if isinstance(expected_timestampset, tuple):
        params = TimestampSet(*expected_timestampset)
    else:
        params = TimestampSet(expected_timestampset)
    await connection.execute("INSERT INTO tbl_timestampset (timetype) VALUES ($1)", params)
    result = await connection.fetchval("SELECT timetype FROM tbl_timestampset WHERE timetype=$1", params)
    if isinstance(expected_timestampset, tuple):
        assert result == TimestampSet(*expected_timestampset)
    else:
        assert result == TimestampSet(expected_timestampset)

@pytest.mark.parametrize('expected_period', [
    '[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01]',
    '[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01)',
    '(2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01]',
    '(2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01)',
    ('2019-09-08 00:00:00+01', '2019-09-10 00:00:00+01'),
    ('2019-09-08 00:00:00+01', '2019-09-10 00:00:00+01', False, True),
    (parse('2019-09-08 00:00:00+01'), parse('2019-09-10 00:00:00+01')),
    (parse('2019-09-08 00:00:00+01'), parse('2019-09-10 00:00:00+01'), False, True),
])
async def test_period_constructor(connection, expected_period):
    if isinstance(expected_period, tuple):
        params = Period(*expected_period)
    else:
        params = Period(expected_period)
    await connection.execute("INSERT INTO tbl_period (timetype) VALUES ($1)", params)
    result = await connection.fetchval("SELECT timetype FROM tbl_period WHERE timetype=$1", params)
    if isinstance(expected_period, tuple):
        assert result == Period(*expected_period)
    else:
        assert result == Period(expected_period)

@pytest.mark.parametrize('expected_periodset', [
    '{[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01]}',
    '{[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01], [2019-09-11 00:00:00+01, 2019-09-12 00:00:00+01]}',
    ['[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01]', '[2019-09-11 00:00:00+01, 2019-09-12 00:00:00+01]'],
    [Period('[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01]'),
     Period('[2019-09-11 00:00:00+01, 2019-09-12 00:00:00+01]')],
    ('[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01]', '[2019-09-11 00:00:00+01, 2019-09-12 00:00:00+01]'),
    (Period('[2019-09-08 00:00:00+01, 2019-09-10 00:00:00+01]'),
     Period('[2019-09-11 00:00:00+01, 2019-09-12 00:00:00+01]')),
])
async def test_periodset_constructor(connection, expected_periodset):
    if isinstance(expected_periodset, tuple):
        params = PeriodSet(*expected_periodset)
    else:
        params = PeriodSet(expected_periodset)
    await connection.execute("INSERT INTO tbl_periodset (timetype) VALUES ($1)", params)
    result = await connection.fetchval("SELECT timetype FROM tbl_periodset WHERE timetype=$1", params)
    if isinstance(expected_periodset, tuple):
        assert result == PeriodSet(*expected_periodset)
    else:
        assert result == PeriodSet(expected_periodset)

