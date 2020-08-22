from parsec import *
from datetime import datetime
from dateutil.parser import parse
from mobilitydb.temporal import Temporal
from mobilitydb.temporal.temporal_parser import parse_temporalinst

from pymeos.io import DeserializerBool
from pymeos.range import RangeBool
from pymeos.temporal import Interpolation, TBoolInst as _TBoolInst, TBoolInstSet as _TBoolInstSet, TBoolSeq as _TBoolSeq, TBoolSeqSet as _TBoolSeqSet


class TBool(Temporal):
    """
    Abstract class for representing temporal Booleans of any duration.
    """

    pymeos_deserializer_type = DeserializerBool
    pymeos_range_type = RangeBool


class TBoolInst(_TBoolInst, TBool):
    """
    Class for representing temporal Booleans of instant duration.

    ``TBoolInst`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TBoolInst('true@2019-09-01')

    Another possibility is to give the ``value`` and the ``time`` arguments,
    which can be instances of ``str``, ``bool``, or ``datetime``.

        >>> TBoolInst('True', '2019-09-08 00:00:00+01')
        >>> TBoolInst(['True', '2019-09-08 00:00:00+01'])
        >>> TBoolInst(True, parse('2019-09-08 00:00:00+01'))
        >>> TBoolInst([True, parse('2019-09-08 00:00:00+01')])

    """


class TBoolI(_TBoolInstSet, TBool):
    """
    Class for representing temporal Booleans of instant set duration.

    ``TBoolI`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TBoolI('AA@2019-09-01')

    Another possibility is to give a set of arguments,
    which can be instances of ``str`` or ``TBoolInst``.

        >>> TBoolI({'AA@2019-09-01 00:00:00+01', 'BB@2019-09-02 00:00:00+01', 'AA@2019-09-03 00:00:00+01'})
        >>> TBoolI({TBoolInst('AA@2019-09-01 00:00:00+01'), TBoolInst('BB@2019-09-02 00:00:00+01'), TBoolInst('AA@2019-09-03 00:00:00+01')})

    """


class TBoolSeq(_TBoolSeq, TBool):
    """
    Class for representing temporal Booleans of sequence duration.

    ``TBoolSeq`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TBoolSeq('[true@2019-09-01 00:00:00+01, false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]')

    Another possibility is to give the arguments as follows.

    * ``instants`` is the set of composing instants, which can be instances of
      ``str`` or ``TBoolInst``,
    * ``lower_inc`` and ``upper_inc`` are instances of ``bool`` specifying
      whether the bounds are inclusive or not. By default ``lower_inc``
      is ``True`` and ``upper_inc`` is ``False``.

    Some examples are given next.

        >>> TBoolSeq({'true@2019-09-01 00:00:00+01', 'false@2019-09-02 00:00:00+01', 'true@2019-09-03 00:00:00+01'})
        >>> TBoolSeq({TBoolInst('true@2019-09-01 00:00:00+01'), TBoolInst('false@2019-09-02 00:00:00+01'), TBoolInst('true@2019-09-03 00:00:00+01')})
        >>> TBoolSeq({'true@2019-09-01 00:00:00+01', 'false@2019-09-02 00:00:00+01', 'true@2019-09-03 00:00:00+01'}, True, True)
        >>> TBoolSeq({TBoolInst('true@2019-09-01 00:00:00+01'), TBoolInst('false@2019-09-02 00:00:00+01'), TBoolInst('true@2019-09-03 00:00:00+01')}, True, True)

    """

    def __init__(self, instants, lower_inc=None, upper_inc=None):
        if isinstance(instants, str):
            super().__init__(instants)
        else:
            super().__init__(instants, lower_inc, upper_inc)


class TBoolS(_TBoolSeqSet, TBool):
    """
    Class for representing temporal Booleans of sequence set duration.

    ``TBoolS`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TBoolS('{[true@2019-09-01 00:00:00+01], [false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]}')

    Another possibility is to give the set of composing sequences, which
    can be instances of ``str`` or ``TBoolSeq``.

        >>> TBoolS({'[true@2019-09-01 00:00:00+01]', '[false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]'})
        >>> TBoolS({TBoolSeq('[true@2019-09-01 00:00:00+01]'), TBoolSeq('[false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]')})

    """

