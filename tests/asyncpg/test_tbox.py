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
from mobilitydb import TBox

pytestmark = pytest.mark.asyncio

@pytest.mark.parametrize('expected_tbox', [
    'TBOX((10.0, 2019-09-08 00:00:00+02), (30.0, 2019-09-10 00:00:00+02))',
    'TBOX((, 2019-09-08 00:00:00+02), (, 2019-09-10 00:00:00+02))',
    'TBOX((10.0, ), (30.0, ))',
    ('10.0', '20.0'),
    (10.0, 20.0),
    ('2019-09-08 00:00:00+01', '2019-09-08 00:00:00+01'),
    (parse('2019-09-08 00:00:00+01'), parse('2019-09-08 00:00:00+01')),
    ('10.0', '2019-09-08 00:00:00+01', '20.0', '2019-09-08 00:00:00+01'),
    (10.0, parse('2019-09-08 00:00:00+01'), 20.0, parse('2019-09-08 00:00:00+01')),
])
async def test_tbox_constructor(connection, expected_tbox):
    if isinstance(expected_tbox, tuple):
        params = TBox(*expected_tbox)
    else:
        params = TBox(expected_tbox)
    print('params =',params.__class__)
    await connection.execute("INSERT INTO tbl_tbox (box) VALUES ($1)", params)
    print('after =',params)
    result = await connection.fetchval("SELECT box FROM tbl_tbox WHERE box=$1", params)
    if isinstance(expected_tbox, tuple):
        assert result == TBox(*expected_tbox)
    else:
        assert result == TBox(expected_tbox)
