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
import psycopg2
import os
from mobilitydb import *
from mobilitydb.psycopg import register

db = psycopg2.connect(dbname=os.getenv('PGDATABASE', 'test'))
db.autocommit = True

register(db)
cur = db.cursor()

time_types = [TimestampSet, Period, PeriodSet]
box_types = [TBox, STBox]
subtype_suffixes = ['Inst', 'InstSet', 'Seq', 'SeqSet']
subtype_names = ['INSTANT', 'INSTANTSET', 'SEQUENCE', 'SEQUENCESET']
temporal_types = [TBool, TInt, TFloat, TText, TGeomPoint, TGeogPoint]

def pytest_configure():
    for time in time_types:
        cur.execute(
            'CREATE TABLE IF NOT EXISTS tbl_' + time.__name__.lower() +
            '(timetype ' +  time.__name__.lower() + ' NOT NULL);')
    for box in box_types:
        cur.execute(
            'CREATE TABLE IF NOT EXISTS tbl_' + box.__name__.lower() +
            '(box ' +  box.__name__.lower() + ' NOT NULL);')
    for ttype in temporal_types:
        for suffix, name in zip(subtype_suffixes, subtype_names):
            cur.execute(
                'CREATE TABLE IF NOT EXISTS tbl_' + ttype.__name__.lower() + suffix +
                '(temp ' + ttype.__name__.lower() + '(' + name + ') NOT NULL);')

def pytest_unconfigure():
    for time in time_types:
        cur.execute(
            'DROP TABLE tbl_' + time.__name__.lower() + ';')
    for box in box_types:
        cur.execute(
            'DROP TABLE tbl_' + box.__name__.lower() + ';')
    for ttype, suffix in zip(temporal_types, subtype_suffixes):
        cur.execute('DROP TABLE tbl_' + ttype.__name__.lower() + suffix + ';')

@pytest.fixture
def cursor():
    # Make sure tables are clean.
    for time in time_types:
        cur.execute('TRUNCATE TABLE tbl_' + time.__name__.lower() + ';')
    for box in box_types:
        cur.execute('TRUNCATE TABLE tbl_' + box.__name__.lower() + ';')
    for ttype in temporal_types:
        for suffix in subtype_suffixes:
            cur.execute('TRUNCATE TABLE tbl_' + ttype.__name__.lower() + suffix + ';')
    return cur
