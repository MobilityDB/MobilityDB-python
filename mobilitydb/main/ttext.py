from datetime import datetime
from dateutil.parser import parse

from pymeos.io import DeserializerText
from pymeos.range import RangeText
from pymeos.temporal import (
    TTextInst as _TTextInst,
    TTextInstSet as _TTextInstSet,
    TTextSeq as _TTextSeq,
    TTextSeqSet as _TTextSeqSet,
)

from mobilitydb.temporal import Temporal


class TText(Temporal):
    """
    Abstract class for representing temporal strings of any duration.
    """

    pymeos_deserializer_type = DeserializerText
    pymeos_range_type = RangeText


class TTextInst(_TTextInst, TText):
    """
    Class for representing temporal strings of instant duration.

    ``TTextInst`` objects can be created 
    with a single argument of type string as in MobilityDB.

        >>> TTextInst('AA@2019-09-01')

    Another possibility is to give the ``value`` and the ``time`` arguments,
    which can be instances of ``str`` or ``datetime``.

        >>> TTextInst('AA', '2019-09-08 00:00:00+01')
        >>> TTextInst(['AA', '2019-09-08 00:00:00+01'])
        >>> TTextInst('AA', parse('2019-09-08 00:00:00+01'))
        >>> TTextInst(['AA', parse('2019-09-08 00:00:00+01')])
    """


class TTextInstSet(_TTextInstSet, TText):
    """
    Class for representing temporal strings of instant set duration.

    ``TTextInstSet`` objects can be created 
    with a single argument of type string as in MobilityDB.

        >>> TTextInstSet('AA@2019-09-01')

    Another possibility is to give a set of composing instants,
    which can be instances of ``str`` or ``TTextInst``.

        >>> TTextInstSet({'AA@2019-09-01 00:00:00+01', 'BB@2019-09-02 00:00:00+01', 'AA@2019-09-03 00:00:00+01'})
        >>> TTextInstSet({TTextInst('AA@2019-09-01 00:00:00+01'), TTextInst('BB@2019-09-02 00:00:00+01'), TTextInst('AA@2019-09-03 00:00:00+01')})
    """


class TTextSeq(_TTextSeq, TText):
    """
    Class for representing temporal strings of sequence duration.

    ``TTextSeq`` objects can be created 
    with a single argument of type string as in MobilityDB.

        >>> TTextSeq('[AA@2019-09-01 00:00:00+01, BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]')

    Another possibility is to give the arguments as follows:

    * ``instants`` is the set of composing instants, which can be instances of
      ``str`` or ``TTextInst``,
    * ``lower_inc`` and ``upper_inc`` are instances of ``bool`` specifying
      whether the bounds are inclusive or not. By default ``lower_inc``
      is ``True`` and ``upper_inc`` is ``False``.

    Some examples are given next.

        >>> TTextSeq({'AA@2019-09-01 00:00:00+01', 'BB@2019-09-02 00:00:00+01', 'AA@2019-09-03 00:00:00+01'})
        >>> TTextSeq({TTextInst('AA@2019-09-01 00:00:00+01'), TTextInst('BB@2019-09-02 00:00:00+01'), TTextInst('AA@2019-09-03 00:00:00+01')})
        >>> TTextSeq({'AA@2019-09-01 00:00:00+01', 'BB@2019-09-02 00:00:00+01', 'AA@2019-09-03 00:00:00+01'}, True, True)
        >>> TTextSeq({TTextInst('AA@2019-09-01 00:00:00+01'), TTextInst('BB@2019-09-02 00:00:00+01'), TTextInst('AA@2019-09-03 00:00:00+01')}, True, True)
    """

    def __init__(self, instants, lower_inc=None, upper_inc=None):
        if isinstance(instants, str):
            super().__init__(instants)
        else:
            super().__init__(instants, lower_inc, upper_inc)


class TTextSeqSet(_TTextSeqSet, TText):
    """
    Class for representing temporal strings of sequence duration.

    ``TTextSeqSet`` objects can be created with a single argument of typestring as in MobilityDB.

        >>> TTextSeqSet('{[AA@2019-09-01 00:00:00+01], [BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]}')

    Another possibility is to give the list of composing sequences, which can be
    instances of ``str`` or ``TTextSeq``.

        >>> TTextSeqSet({'[AA@2019-09-01 00:00:00+01]', '[BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]'})
        >>> TTextSeqSet({TTextSeq('[AA@2019-09-01 00:00:00+01]'), TTextSeq('[BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]')})
    """
