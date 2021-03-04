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
import asyncio
from dateutil.parser import parse
from mobilitydb import STBox

pytestmark = pytest.mark.asyncio

@pytest.mark.parametrize('expected_stbox', [
    # Only coordinate (X and Y) dimension
    'STBOX ((1.0, 2.0), (1.0, 2.0))',
    (('1.0', '2.0', '3.0', '4.0')),
    (1.0, 2.0, 3.0, 4.0),
    # Only coordinate (X, Y and Z) dimension
    'STBOX Z((1.0, 2.0, 3.0), (1.0, 2.0, 3.0))',
    (('1.0', '2.0', '3.0', '4.0', '5.0', '6.0')),
    ((1.0, 2.0, 3.0, 4.0, 5.0, 6.0)),
    # Both coordinate (X, Y) and time dimensions
    'STBOX T((1.0, 2.0, 2001-01-03 00:00:00+01), (1.0, 2.0, 2001-01-03 00:00:00+01))',
    {'bounds':(1.0, 2.0, '2001-01-01 00:00:00+01', 3.0, 4.0, '2001-01-02 00:00:00+01'), 'dimt':True},
    {'bounds':(1.0, 2.0, parse('2001-01-01 00:00:00+01'), 3.0, 4.0, parse('2001-01-02 00:00:00+01')), 'dimt':True},
    # Both coordinate (X, Y, and Z) and time dimensions
    'STBOX ZT((1.0, 2.0, 3.0, 2001-01-04 00:00:00+01), (1.0, 2.0, 3.0, 2001-01-04 00:00:00+01))',
    ((1.0, 2.0, 3.0, '2001-01-01 00:00:00+01', 4.0, 5.0, 6.0, '2001-01-02 00:00:00+01')),
    ((1.0, 2.0, 3.0, parse('2001-01-01 00:00:00+01'), 4.0, 5.0, 6.0, parse('2001-01-02 00:00:00+01'))),
    # Only time dimension
    'STBOX T(, 2001-01-03 00:00:00+01), (, 2001-01-03 00:00:00+01))',
    (('2001-01-03 00:00:00+01', '2001-01-03 00:00:00+01')),
    ((parse('2001-01-03 00:00:00+01'), parse('2001-01-03 00:00:00+01'))),
    # Only geodetic coordinate (X, Y and Z) dimension
    'GEODSTBOX((1.0, 2.0, 3.0), (1.0, 2.0, 3.0))',
    {'bounds':(1.0, 2.0, 3.0, 4.0, 5.0, 6.0), 'geodetic':True},
    #  Both geodetic coordinate (X, Y, and Z) and time dimensions
    'GEODSTBOX T((1.0, 2.0, 3.0, 2001-01-03 00:00:00+01), (1.0, 2.0, 3.0, 2001-01-04 00:00:00+01))',
    {'bounds':(1.0, 2.0, 3.0, '2001-01-01 00:00:00+01', 4.0, 5.0, 6.0, '2001-01-02 00:00:00+01'), 'geodetic':True},
    # Only time dimension for geodetic box
    'GEODSTBOX T((, 2001-01-03 00:00:00+01), (, 2001-01-03 00:00:00+01))',
    {'bounds':('2001-01-01 00:00:00+01', '2001-01-02 00:00:00+01'), 'geodetic':True},
    # With SRID
    'SRID=5676;STBOX T((1.0, 2.0, 2001-01-04 00:00:00+01), (1.0, 2.0, 2001-01-04 00:00:00+01))',
    'SRID=4326;GEODSTBOX((1.0, 2.0, 3.0), (1.0, 2.0, 3.0))',
    {'bounds': (1.0, 2.0, 3.0, '2001-01-01 00:00:00+01', 4.0, 5.0, 6.0, '2001-01-02 00:00:00+01'), 'geodetic': True, 'srid': 4326},
])
async def test_stbox_constructor(connection, expected_stbox):
    if isinstance(expected_stbox, dict):
        params = STBox(**expected_stbox)
    else:
        params = STBox(expected_stbox)
    print(params.__class__)
    print(params.xmax)
    await connection.execute("INSERT INTO tbl_stbox (box) VALUES ($1)", params)
    result = await connection.fetchval("SELECT box FROM tbl_stbox WHERE box=$1", params, column=0)
    if isinstance(expected_stbox, dict):
        assert result == STBox(**expected_stbox)
    else:
        assert result == STBox(expected_stbox)
