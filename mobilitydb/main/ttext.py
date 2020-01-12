from datetime import datetime
from dateutil.parser import parse
from mobilitydb.temporal.temporal_parser import parse_temporalinst
from mobilitydb.temporal import Temporal, TemporalInst, TemporalI, TemporalSeq, TemporalS


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
            raise ValueError('TText value must subclass TText class')
        return value.__str__().strip("'")


class TTextInst(TemporalInst, TText):
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

    """It is not possible to call super().__init__(value, time) since it is necessary
    to strip the eventual double quotes enclosing the value
    """

    def __init__(self, value, time=None):
        TemporalInst.BaseClass = str
        if(time is None):
            # Constructor with a single argument of type string
            if (isinstance(value, str)):
                couple = parse_temporalinst(value, 0)
                value = couple[2][0]
                time = couple[2][1]
            # Constructor with a single argument of type tuple or list
            elif (isinstance(value, (tuple, list))):
                value, time = value
            else:
                raise Exception("ERROR: Could not parse temporal instant value")
        # Now both value and time are not None
        assert(isinstance(value, str)), "ERROR: Invalid value argument"
        assert(isinstance(time, (str, datetime))), "ERROR: Invalid time argument"
        # Remove double quotes if present
        if value[0] == '"' and value[-1] == '"':
            value = value[1:-1]
        self._value = value
        self._time = parse(time) if isinstance(time, str) else time


class TTextI(TemporalI, TText):
    """
    Class for representing temporal strings of instant set duration.

    ``TTextI`` objects can be created 
    with a single argument of type string as in MobilityDB.

        >>> TTextI('AA@2019-09-01')

    Another possibility is to give a tuple or list of composing instants,
    which can be instances of ``str`` or ``TTextInst``.

        >>> TTextI('AA@2019-09-01 00:00:00+01', 'BB@2019-09-02 00:00:00+01', 'AA@2019-09-03 00:00:00+01')
        >>> TTextI(TTextInst('AA@2019-09-01 00:00:00+01'), TTextInst('BB@2019-09-02 00:00:00+01'), TTextInst('AA@2019-09-03 00:00:00+01'))
        >>> TTextI(['AA@2019-09-01 00:00:00+01', 'BB@2019-09-02 00:00:00+01', 'AA@2019-09-03 00:00:00+01'])
        >>> TTextI([TTextInst('AA@2019-09-01 00:00:00+01'), TTextInst('BB@2019-09-02 00:00:00+01'), TTextInst('AA@2019-09-03 00:00:00+01')])

    """

    def __init__(self,  *argv):
        TemporalI.BaseClass = str
        TemporalI.ComponentClass = TTextInst
        super().__init__(*argv)


class TTextSeq(TemporalSeq, TText):
    """
    Class for representing temporal strings of sequence duration.

    ``TTextSeq`` objects can be created 
    with a single argument of type string as in MobilityDB.

        >>> TTextSeq('[AA@2019-09-01 00:00:00+01, BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]')

    Another possibility is to give the arguments as follows:

    * ``instantList`` is the list of composing instants, which can be instances of
      ``str`` or ``TTextInst``,
    * ``lower_inc`` and ``upper_inc`` are instances of ``bool`` specifying
      whether the bounds are inclusive or not. By default ``lower_inc``
      is ``True`` and ``upper_inc`` is ``False``.

    Some examples are given next.

        >>> TTextSeq(['AA@2019-09-01 00:00:00+01', 'BB@2019-09-02 00:00:00+01', 'AA@2019-09-03 00:00:00+01'])
        >>> TTextSeq(TTextInst('AA@2019-09-01 00:00:00+01'), TTextInst('BB@2019-09-02 00:00:00+01'), TTextInst('AA@2019-09-03 00:00:00+01')])
        >>> TTextSeq(['AA@2019-09-01 00:00:00+01', 'BB@2019-09-02 00:00:00+01', 'AA@2019-09-03 00:00:00+01'], True, True)
        >>> TTextSeq([TTextInst('AA@2019-09-01 00:00:00+01'), TTextInst('BB@2019-09-02 00:00:00+01'), TTextInst('AA@2019-09-03 00:00:00+01')], True, True)

    """

    def __init__(self, instantList, lower_inc=None, upper_inc=None):
        TemporalSeq.BaseClass = str
        TemporalS.BaseClassDiscrete = True
        TemporalSeq.ComponentClass = TTextInst
        super().__init__(instantList, lower_inc, upper_inc)

    @classmethod
    @property
    def interpolation(self):
        """
        Interpolation of the temporal value, that is, ``'Stepwise'``.
        """
        return 'Stepwise'


class TTextS(TemporalS, TText):
    """
    Class for representing temporal strings of sequence duration.

    ``TTextS`` objects can be created with a single argument of typestring as in MobilityDB.

        >>> TTextS('{[AA@2019-09-01 00:00:00+01], [BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]}')

    Another possibility is to give the list of composing sequences, which can be
    instances of ``str`` or ``TTextSeq``.

        >>> TTextS(['[AA@2019-09-01 00:00:00+01]', '[BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]'])
        >>> TTextS([TTextSeq('[AA@2019-09-01 00:00:00+01]'), TTextSeq('[BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]')])
        >>> TTextS([TTextSeq('[AA@2019-09-01 00:00:00+01]'), TTextSeq('[BB@2019-09-02 00:00:00+01, AA@2019-09-03 00:00:00+01]')])

    """

    def __init__(self, sequenceList):
        TemporalS.BaseClass = str
        TemporalS.BaseClassDiscrete = True
        TemporalS.ComponentClass = TTextSeq
        super().__init__(sequenceList)

    @classmethod
    @property
    def interpolation(self):
        """
        Interpolation of the temporal value, that is, ``'Stepwise'``.
        """
        return 'Stepwise'


