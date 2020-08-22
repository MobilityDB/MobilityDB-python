from mobilitydb.temporal import Temporal

from pymeos.io import DeserializerFloat
from pymeos.range import RangeFloat
from pymeos.temporal import Interpolation, TFloatInst as _TFloatInst, TFloatInstSet as _TFloatInstSet, TFloatSeq as _TFloatSeq, TFloatSeqSet as _TFloatSeqSet


class TFloat(Temporal):
    """
    Abstract class for representing temporal floats of any duration.
    """

    pymeos_deserializer_type = DeserializerFloat
    pymeos_range_type = RangeFloat

    @property
    def valueRange(self):
        """
        Range of values taken by the temporal value as defined by its minimum and maximum value
        """
        return RangeFloat(self.minValue, self.maxValue, True, True)


class TFloatInst(_TFloatInst, TFloat):
    """
    Class for representing temporal floats of instant duration.

    ``TFloatInst`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TFloatInst('10.0@2019-09-01')

    Another possibility is to give the ``value`` and the ``time`` arguments,
    which can be instances of ``str``, ``float`` or ``datetime``.

        >>> TFloatInst('10.0', '2019-09-08 00:00:00+01')
        >>> TFloatInst(['10.0', '2019-09-08 00:00:00+01'])
        >>> TFloatInst(10.0, parse('2019-09-08 00:00:00+01'))
        >>> TFloatInst([10.0, parse('2019-09-08 00:00:00+01')])

    """


class TFloatI(_TFloatInstSet, TFloat):
    """
    Class for representing temporal floats of instant set duration.

    ``TFloatI`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TFloatI('10.0@2019-09-01')

    Another possibility is to give a tuple or set of composing instants,
    which can be instances of ``str`` or ``TFloatInst``.

        >>> TFloatI({'10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'})
        >>> TFloatI({TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'), TFloatInst('10.0@2019-09-03 00:00:00+01')})

    """


class TFloatSeq(_TFloatSeq, TFloat):
    """
    Class for representing temporal floats of sequence duration.

    ``TFloatSeq`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TFloatSeq('[10.0@2019-09-01 00:00:00+01, 20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]')
        >>> TFloatSeq('Interp=Stepwise;[10.0@2019-09-01 00:00:00+01, 20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]')

    Another possibility is to give the arguments as follows:

    * ``instants`` is the set of composing instants, which can be instances of
      ``str`` or ``TFloatInst``,
    * ``lower_inc`` and ``upper_inc`` are instances of ``bool`` specifying
      whether the bounds are inclusive or not. By default ``lower_inc``
      is ``True`` and ``upper_inc`` is ``False``.
    * ``interp`` which is either ``'Linear'`` or ``'Stepwise'``, the former being
      the default.

    Some examples are shown next.

        >>> TFloatSeq({'10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'})
        >>> TFloatSeq({TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'), TFloatInst('10.0@2019-09-03 00:00:00+01')})
        >>> TFloatSeq({'10.0@2019-09-01 00:00:00+01', '20.0@2019-09-02 00:00:00+01', '10.0@2019-09-03 00:00:00+01'}, True, True, 'Stepwise')
        >>> TFloatSeq({TFloatInst('10.0@2019-09-01 00:00:00+01'), TFloatInst('20.0@2019-09-02 00:00:00+01'}, TFloatInst('10.0@2019-09-03 00:00:00+01')], True, True, 'Stepwise')

    """

    def __init__(self, instants, lower_inc=None, upper_inc=None, interp=None):
        if isinstance(instants, str) or lower_inc is None:
            super().__init__(instants)
        elif interp is None:
            super().__init__(instants, lower_inc, upper_inc)
        else:
            super().__init__(instants, lower_inc, upper_inc, Interpolation.__members__.get(interp, None))


class TFloatS(_TFloatSeqSet, TFloat):
    """
    Class for representing temporal floats of sequence duration.

    ``TFloatS`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TFloatS('{[10.0@2019-09-01 00:00:00+01], [20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]}')
        >>> TFloatS('Interp=Stepwise;{[10.0@2019-09-01 00:00:00+01], [20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]}')

    Another possibility is to give the arguments as follows:

    * ``sequences`` is a set of composing sequences, which can be
      instances of ``str`` or ``TFloatSeq``,
    * ``interp`` can be ``'Linear'`` or ``'Stepwise'``, the former being
      the default.

    Some examples are shown next.

        >>> TFloatS({'[10.0@2019-09-01 00:00:00+01]', '[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]'})
        >>> TFloatS({'[10.0@2019-09-01 00:00:00+01]', '[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]'}, 'Linear')
        >>> TFloatS({'Interp=Stepwise;[10.0@2019-09-01 00:00:00+01]', 'Interp=Stepwise;[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]'}, 'Stepwise')
        >>> TFloatS({TFloatSeq('[10.0@2019-09-01 00:00:00+01]'), TFloatSeq('[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]')})
        >>> TFloatS({TFloatSeq('[10.0@2019-09-01 00:00:00+01]'),  TFloatSeq('[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]')}, 'Linear')
        >>> TFloatS({TFloatSeq('Interp=Stepwise;[10.0@2019-09-01 00:00:00+01]'), TFloatSeq('Interp=Stepwise;[20.0@2019-09-02 00:00:00+01, 10.0@2019-09-03 00:00:00+01]')}, 'Stepwise')

    """

    def __init__(self, sequences, interp=None):
        if isinstance(sequences, str) or interp is None:
            super().__init__(sequences)
        else:
            super().__init__(sequences, Interpolation.__members__.get(interp))

