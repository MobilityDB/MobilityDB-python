from spans.types import intrange
from mobilitydb.temporal import Temporal, TInstant, TInstantSet, TSequence, TSequenceSet


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
                return TIntSeqSet(value)
            else:
                return TIntInstSet(value)
        raise Exception("ERROR: Could not parse temporal integer value")

    @staticmethod
    def write(value):
        if not isinstance(value, TInt):
            raise ValueError('Value must be an instance of a subclass of TInt')
        return value.__str__().strip("'")

    @property
    def valueRange(self):
        """
        Range of values taken by the temporal value as defined by its minimum and maximum value
        """
        return intrange(self.minValue, self.maxValue, True, True)


class TIntInst(TInstant, TInt):
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

    def __init__(self, value, time=None):
        TInstant.BaseClass = int
        super().__init__(value, time)


class TIntInstSet(TInstantSet, TInt):
    """
    Class for representing temporal integers of instant set duration.

    ``TIntInstSet`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TIntInstSet('10@2019-09-01')

    Another possibility is to give a tuple or list of composing instants,
    which can be instances of ``str`` or ``TIntInst``.

        >>> TIntInstSet('10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '10@2019-09-03 00:00:00+01')
        >>> TIntInstSet(TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'), TIntInst('10@2019-09-03 00:00:00+01'))
        >>> TIntInstSet(['10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '10@2019-09-03 00:00:00+01'])
        >>> TIntInstSet([TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'), TIntInst('10@2019-09-03 00:00:00+01')])

    """

    def __init__(self,  *argv):
        TInstantSet.BaseClass = int
        TInstantSet.ComponentClass = TIntInst
        super().__init__(*argv)


class TIntSeq(TSequence, TInt):
    """
    Class for representing temporal integers of sequence duration.

    ``TIntSeq`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TIntSeq('[10@2019-09-01 00:00:00+01, 20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]')

    Another possibility is to give the arguments as follows:

    * ``instantList`` is the list of composing instants, which can be instances of
      ``str`` or ``TIntInst``,
    * ``lower_inc`` and ``upper_inc`` are instances of ``bool`` specifying
      whether the bounds are inclusive or not. By default ``lower_inc``
      is ``True`` and ``upper_inc`` is ``False``.

    Some examples are given next.

        >>> TIntSeq(['10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '10@2019-09-03 00:00:00+01'])
        >>> TIntSeq([TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'), TIntInst('10@2019-09-03 00:00:00+01')])
        >>> TIntSeq(['10@2019-09-01 00:00:00+01', '20@2019-09-02 00:00:00+01', '10@2019-09-03 00:00:00+01'], True, True)
        >>> TIntSeq([TIntInst('10@2019-09-01 00:00:00+01'), TIntInst('20@2019-09-02 00:00:00+01'), TIntInst('10@2019-09-03 00:00:00+01')], True, True)

    """

    def __init__(self, instantList, lower_inc=None, upper_inc=None):
        TSequence.BaseClass = int
        TSequence.BaseClassDiscrete = True
        TSequence.ComponentClass = TIntInst
        super().__init__(instantList, lower_inc, upper_inc)

    @classmethod
    @property
    def interpolation(self):
        """
        Interpolation of the temporal value, that is, ``'Stepwise'``.
        """
        return 'Stepwise'


class TIntSeqSet(TSequenceSet, TInt):
    """
    Class for representing temporal integers of sequence duration.

    ``TIntSeqSet`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TIntSeqSet('{[10@2019-09-01 00:00:00+01], [20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]}')

    Another possibility is to give the list of composing sequences, which
    can be instances of ``str`` or ``TIntSeq``.

        >>> TIntSeqSet(['[10@2019-09-01 00:00:00+01]', '[20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]'])
        >>> TIntSeqSet([TIntSeq('[10@2019-09-01 00:00:00+01]'), TIntSeq('[20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]')])
        >>> TIntSeqSet([TIntSeq('[10@2019-09-01 00:00:00+01]'), TIntSeq('[20@2019-09-02 00:00:00+01, 10@2019-09-03 00:00:00+01]')])

    """

    def __init__(self, sequenceList):
        TSequenceSet.BaseClass = int
        TSequenceSet.BaseClassDiscrete = True
        TSequenceSet.ComponentClass = TIntSeq
        super().__init__(sequenceList)

    @classmethod
    @property
    def interpolation(self):
        """
        Interpolation of the temporal value, that is, ``'Stepwise'``.
        """
        return 'Stepwise'

