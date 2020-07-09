from datetime import datetime
from dateutil.parser import parse
from mobilitydb.temporal.temporal_parser import parse_temporalinst
from mobilitydb.temporal import Temporal

from pymeos.temporal import TInstantText, TInstantSetText, TSequenceText, TSequenceSetText


class TText(Temporal):
    """
    Abstract class for representing temporal strings of any duration.
    """

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        if value[0] != '{' and value[0] != '[' and value[0] != '(':
            return TTextInst(value)
        elif value[0] == '[' or value[0] == '(':
            return TTextSeq(value)
        elif value[0] == '{':
            if value[1] == '[' or value[1] == '(':
                return TTextS(value)
            else:
                return TTextI(value)
        raise Exception("ERROR: Could not parse temporal text value")

    @staticmethod
    def write(value):
        if not isinstance(value, TText):
            raise ValueError('Value must be an instance of a subclass of TText')
        return value.__str__()


class TTextInst(TInstantText, TText):
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

    def __repr__(self):
        return (f'{self.__class__.__name__ }'
                f'({self.getValue!r}, {self.getTimestamp!r})')


class TTextI(TInstantSetText, TText):
    """
    Class for representing temporal strings of instant set duration.

    ``TTextI`` objects can be created 
    with a single argument of type string as in MobilityDB.

        >>> TTextI('AA@2019-09-01')

    Another possibility is to give a set of composing instants,
    which can be instances of ``str`` or ``TTextInst``.

        >>> TTextI({'AA@2019-09-01 00:00:00+01', 'BB@2019-09-02 00:00:00+01', 'AA@2019-09-03 00:00:00+01'})
        >>> TTextI({TTextInst('AA@2019-09-01 00:00:00+01'), TTextInst('BB@2019-09-02 00:00:00+01'), TTextInst('AA@2019-09-03 00:00:00+01')})

    """

    def __repr__(self):
        return (f'{self.__class__.__name__ }'
                f'({self.instants!r})')


class TTextSeq(TSequenceText, TText):
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

    @classmethod
    @property
    def interpolation(self):
        """
        Interpolation of the temporal value, that is, ``'Stepwise'``.
        """
        return 'Stepwise'

    def __repr__(self):
        return (f'{self.__class__.__name__ }'
                f'({self.instants!r}, {self.lower_inc!r}, {self.upper_inc!r})')


class TTextS(TSequenceSetText, TText):
    """
    Class for representing temporal strings of sequence duration.

    ``TTextS`` objects can be created with a single argument of typestring as in MobilityDB.

        >>> TTextS('{[AA@2019-09-01 00:00:00+01], [BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]}')

    Another possibility is to give the list of composing sequences, which can be
    instances of ``str`` or ``TTextSeq``.

        >>> TTextS({'[AA@2019-09-01 00:00:00+01]', '[BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]'})
        >>> TTextS({TTextSeq('[AA@2019-09-01 00:00:00+01]'), TTextSeq('[BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]')})

    """

    @classmethod
    @property
    def interpolation(self):
        """
        Interpolation of the temporal value, that is, ``'Stepwise'``.
        """
        return 'Stepwise'

    def __repr__(self):
        return (f'{self.__class__.__name__ }'
                f'({self.sequences!r})')


