from spans.types import floatrange
from mobilitydb.temporal import Temporal

from pymeos.temporal import Interpolation, TInstantFloat, TInstantSetFloat, TSequenceFloat, TSequenceSetFloat


class TFloat(Temporal):
    """
    Abstract class for representing temporal floats of any duration.
    """

    @property
    def valueRange(self):
        """
        Range of values taken by the temporal value as defined by its minimum and maximum value
        """
        # Should we return postgis's floatrange or PyMEOS's RangeFloat?
        # Note that because of duck typing both are substitutable for each other
        return floatrange(self.minValue, self.maxValue, True, True)

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        if value.startswith('Interp=Stepwise;'):
            value1 = value.replace('Interp=Stepwise;', '')
            if value1[0] == '{':
                return TFloatS(value)
            else:
                return TFloatSeq(value)
        elif value[0] != '{' and value[0] != '[' and value[0] != '(':
            return TFloatInst(value)
        elif value[0] == '[' or value[0] == '(':
            return TFloatSeq(value)
        elif value[0] == '{':
            if value[1] == '[' or value[1] == '(':
                return TFloatS(value)
            else:
                return TFloatI(value)
        raise Exception("ERROR: Could not parse temporal float value")

    @staticmethod
    def write(value):
        if not isinstance(value, TFloat):
            raise ValueError('Value must be an instance of a subclass of TFloat')
        return value.__str__()


class TFloatInst(TInstantFloat, TFloat):
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


class TFloatI(TInstantSetFloat, TFloat):
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


class TFloatSeq(TSequenceFloat, TFloat):
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


class TFloatS(TSequenceSetFloat, TFloat):
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
        # TODO support interp
        super().__init__(sequences)

    @property
    def interpolation(self):
        """
        Interpolation of the temporal value, which is either ``'Linear'`` or ``'Stepwise'``.
        """
        return self._interp

