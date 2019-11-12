# MobilityDB helpers for psycopg2.
import psycopg2
from MobilityDB.MainTypes import *
from MobilityDB.TimeTypes import *
from MobilityDB.MobilityDBConnection import MobilityDBRegister, MobilityDB

__all__ = ['psycopg2', 'MobilityDBRegister',
           'TGEOMPOINT', 'TGEOMPOINTINST', 'TGEOMPOINTI', 'TGEOMPOINTSEQ', 'TGEOMPOINTS',
           'TINT', 'TINTINST', 'TINTI', 'TINTSEQ', 'TINTS',
           'TFLOAT', 'TFLOATINST', 'TFLOATI', 'TFLOATSEQ', 'TFLOATS',
           'TBOOL', 'TBOOLINST', 'TBOOLI', 'TBOOLSEQ', 'TBOOLS',
           'TTEXT', 'TTEXTINST', 'TTEXTI', 'TTEXTSEQ', 'TTEXTS',
           'PERIOD', 'TIMESTAMPSET', 'PERIODSET']

try:
    import pkg_resources
except ImportError:  # pragma: no cover
    pass

