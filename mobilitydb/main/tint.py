from spans.types import intrange
from mobilitydb.temporal import Temporal, TemporalInst, TemporalI, TemporalSeq, TemporalS


class TInt(Temporal):
    """
    Abstract class for representing temporal integers of any duration.
    """

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        if value[0] != '{' and value[0] != '[' and value[0] != '(':
            return TIntInst(value)
        elif value[0] == '[' or value[0] == '(':
            return TIntSeq(value)
        elif value[0] == '{':
            if value[1] == '[' or value[1] == '(':
                return TIntS(value)
            else:
                return TIntI(value)
        raise Exception("ERROR: Could not parse temporal integer value")

    @staticmethod
    def write(value):
        if not isinstance(value, TInt):
            raise ValueError('TInt value must subclass TInt class')
        return value.__str__().strip("'")

    @property
    def valueRange(self):
        """
        Distinct values
        """
        return intrange(self.minValue, self.maxValue, True, True)


class TIntInst(TemporalInst, TInt):
    """
    Class for representing temporal floats of instant duration.

    ``TIntInst`` objects can be created in a number of ways. One possibility is
    with a single argument of type string as in MobilityDB.

        >>> TIntInst('10@2019-09-01')

    Another possibility is to give the ``value`` and the ``time`` arguments,
    which can be instances of ``str``, ``int`` and ``datetime``.

        >>> TIntInst('10', '2019-09-08 00:00:00+01')
        >>> TIntInst(['10', '2019-09-08 00:00:00+01'])
        >>> TIntInst(10, parse('2019-09-08 00:00:00+01'))
        >>> TIntInst([10, parse('2019-09-08 00:00:00+01')])

    """

    def __init__(self, value, time=None):
        TemporalInst.BaseClass = int
        super().__init__(value, time)


class TIntI(TemporalI, TInt):
    """
    Class for representing temporal integers of instant set duration.

    ``TIntI`` objects can be created in a number of ways. One possibility is
    with a single argument of type string as in MobilityDB.

        >>> TIntI('10@2019-09-01')

    Another possibility is to give a tuple or list of arguments,
    which can be instances of ``str`` or ``TIntInst``.

        >>> TIntI('10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '10@2019-09-03 00:00:00+01')
        >>> TIntI(TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'), TIntInst('10@2019-09-03 00:00:00+01'))
        >>> TIntI(['10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '10@2019-09-03 00:00:00+01'])
        >>> TIntI([TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'), TIntInst('10@2019-09-03 00:00:00+01')])

    """

    def __init__(self,  *argv):
        TemporalI.BaseClass = int
        TemporalI.ComponentClass = TIntInst
        super().__init__(*argv)


class TIntSeq(TemporalSeq, TInt):
    """
    Class for representing temporal floats of sequence duration.

    ``TIntSeq`` objects can be created in a number of ways. One possibility is
    with a single argument of type string as in MobilityDB.

        >>> TIntSeq('[10@2019-09-01 00:00:00+01, 20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]')

    Another possibility is to give the ``instantList``, ``lower_inc``,
    ``upper_inc``, and ``interp`` arguments, where

    * the instants in ``instantList`` can be instances of ``str`` or ``TIntInst``,
    * ``lower_inc`` and ``upper_inc`` are instances of ``bool``, where by default
    ``lower_inc`` is ``True`` and ``upper_inc`` is ``False``

        >>> TIntSeq(['10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '10@2019-09-03 00:00:00+01'])
        >>> TIntSeq([TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'), TIntInst('10@2019-09-03 00:00:00+01')])
        >>> TIntSeq(['10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '10@2019-09-03 00:00:00+01'], True, True)
        >>> TIntSeq([TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'), TIntInst('10@2019-09-03 00:00:00+01')], True, True)

    """

    def __init__(self, instantList, lower_inc=None, upper_inc=None):
        TemporalSeq.BaseClass = int
        TemporalSeq.BaseClassDiscrete = True
        TemporalSeq.ComponentClass = TIntInst
        super().__init__(instantList, lower_inc, upper_inc)

    @classmethod
    @property
    def interpolation(self):
        """
        Interpolation for the temporal sequence
        """
        return 'Stepwise'


class TIntS(TemporalS, TInt):
    """
    Class for representing temporal floats of sequence duration.

    ``TIntS`` objects can be created in a number of ways. One possibility is
    with a single argument of type string as in MobilityDB.

        >>> TIntS('{[10@2019-09-01 00:00:00+01], [20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]}')

    Another possibility is to give the ``instantList``, ``lower_inc``,
    ``upper_inc``, and ``interp`` arguments, where the sequences in
    ``sequenceList`` can be instances of ``str`` or ``TIntSeq``.

        >>> TIntS(['[10@2019-09-01 00:00:00+01]', '[20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]'])
        >>> TIntS([TIntSeq('[10@2019-09-01 00:00:00+01]'), TIntSeq('[20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]')])
        >>> TIntS([TIntSeq('[10@2019-09-01 00:00:00+01]'), TIntSeq('[20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]')])

    """

    def __init__(self, sequenceList):
        TemporalS.BaseClass = int
        TemporalS.BaseClassDiscrete = True
        TemporalS.ComponentClass = TIntSeq
        super().__init__(sequenceList)

    @classmethod
    @property
    def interpolation(self):
        """
        Interpolation for the temporal sequence set
        """
        return 'Stepwise'

