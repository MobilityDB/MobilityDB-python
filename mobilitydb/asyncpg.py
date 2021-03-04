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

import asyncio
import asyncpg
from mobilitydb.time import TimestampSet, Period, PeriodSet
from mobilitydb.boxes import TBox, STBox
from mobilitydb.main import TBool, TInt, TFloat, TText, TGeomPoint, TGeogPoint

# Suggestion is to have our own connection method to register our types without asking the user to do this step
"""
class MobilityDB:
    @classmethod
    async def connect(cls, host_, database_, user_, password_):
        conn = await asyncpg.connect(host=host_, database=database_, user=user_, password=password_)
        register(conn)
        return conn
"""

async def register(conn):
    # Add MobilityDB types to PostgreSQL adapter and specify the encoder and decoder functions for each type.
    await conn.set_type_codec("timestampset", encoder=TimestampSet.write, decoder=TimestampSet.read_from_cursor)
    await conn.set_type_codec("period", encoder=Period.write, decoder=Period.read_from_cursor)
    await conn.set_type_codec("periodset", encoder=PeriodSet.write, decoder=PeriodSet.read_from_cursor)
    await conn.set_type_codec("tbox", encoder=TBox.write, decoder=TBox.read_from_cursor)
    await conn.set_type_codec("tbool", encoder=TBool.write, decoder=TBool.read_from_cursor)
    await conn.set_type_codec("tint", encoder=TInt.write, decoder=TInt.read_from_cursor)
    await conn.set_type_codec("tfloat", encoder=TFloat.write, decoder=TFloat.read_from_cursor)
    await conn.set_type_codec("ttext", encoder=TText.write, decoder=TText.read_from_cursor)
    await conn.set_type_codec("stbox", encoder=STBox.write, decoder=STBox.read_from_cursor)
    await conn.set_type_codec("tgeompoint", encoder=TGeomPoint.write, decoder=TGeomPoint.read_from_cursor)
    await conn.set_type_codec("tgeogpoint", encoder=TGeogPoint.write, decoder=TGeogPoint.read_from_cursor)
