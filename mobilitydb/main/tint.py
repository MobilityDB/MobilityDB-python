from pymeos.io import DeserializerInt
from pymeos.range import RangeInt
from pymeos.temporal import TIntInst as _TIntInst, TIntInstSet as _TIntInstSet, TIntSeq as _TIntSeq, TIntSeqSet as _TIntSeqSet

from mobilitydb.temporal import Temporal


class TInt(Temporal):
    """
    Abstract class for representing temporal integers of any duration.
    """

    pymeos_deserializer_type = DeserializerInt
    pymeos_range_type = RangeInt

    @property
    def valueRange(self):
        """
        Range of values taken by the temporal value as defined by its minimum and maximum value
        """
        return RangeInt(self.minValue, self.maxValue, True, True)


class TIntInst(_TIntInst, TInt):
    """
    Class for representing temporal integers of instant duration.

    ``TIntInst`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TIntInst('10@2019-09-01')

    Another possibility is to give the ``value`` and the ``time`` arguments,
    which can be instances of ``str``, ``int`` or ``datetime``.

        >>> TIntInst('10', '2019-09-08 00:00:00+01')
        >>> TIntInst(['10', '2019-09-08 00:00:00+01'])
        >>> TIntInst(10, parse('2019-09-08 00:00:00+01'))
        >>> TIntInst([10, parse('2019-09-08 00:00:00+01')])
    """


class TIntInstSet(_TIntInstSet, TInt):
    """
    Class for representing temporal integers of instant set duration.

    ``TIntInstSet`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TIntInstSet('10@2019-09-01')

    Another possibility is to give a tuple or set of composing instants,
    which can be instances of ``str`` or ``TIntInst``.

        >>> TIntInstSet({'10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '10@2019-09-03 00:00:00+01'})
        >>> TIntInstSet({TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'), TIntInst('10@2019-09-03 00:00:00+01')})
    """


class TIntSeq(_TIntSeq, TInt):
    """
    Class for representing temporal integers of sequence duration.

    ``TIntSeq`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TIntSeq('[10@2019-09-01 00:00:00+01, 20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]')

    Another possibility is to give the arguments as follows:

    * ``instants`` is the set of composing instants, which can be instances of
      ``str`` or ``TIntInst``,
    * ``lower_inc`` and ``upper_inc`` are instances of ``bool`` specifying
      whether the bounds are inclusive or not. By default ``lower_inc``
      is ``True`` and ``upper_inc`` is ``False``.

    Some examples are given next.

        >>> TIntSeq({'10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '10@2019-09-03 00:00:00+01'})
        >>> TIntSeq({TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'), TIntInst('10@2019-09-03 00:00:00+01')})
        >>> TIntSeq({'10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '10@2019-09-03 00:00:00+01'}, True, True)
        >>> TIntSeq({TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'), TIntInst('10@2019-09-03 00:00:00+01')}, True, True)
    """

    def __init__(self, instants, lower_inc=None, upper_inc=None):
        if isinstance(instants, str):
            super().__init__(instants)
        else:
            super().__init__(instants, lower_inc, upper_inc)


class TIntSeqSet(_TIntSeqSet, TInt):
    """
    Class for representing temporal integers of sequence duration.

    ``TIntSeqSet`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TIntSeqSet('{[10@2019-09-01 00:00:00+01], [20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]}')

    Another possibility is to give the set of composing sequences, which
    can be instances of ``str`` or ``TIntSeq``.

        >>> TIntSeqSet({'[10@2019-09-01 00:00:00+01]', '[20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]'})
        >>> TIntSeqSet({TIntSeq('[10@2019-09-01 00:00:00+01]'), TIntSeq('[20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]')})
    """

