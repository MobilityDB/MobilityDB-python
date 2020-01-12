from parsec import *
from datetime import datetime
from dateutil.parser import parse
from mobilitydb.temporal import Temporal, TemporalInst, TemporalI, TemporalSeq, TemporalS
from mobilitydb.temporal.temporal_parser import parse_temporalinst


class TBool(Temporal):
    """
    Abstract class for representing temporal Booleans of any duration.
    """

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        if value[0] != '{' and value[0] != '[' and value[0] != '(':
            return TBoolInst(value)
        elif value[0] == '[' or value[0] == '(':
            return TBoolSeq(value)
        elif value[0] == '{':
            if value[1] == '[' or value[1] == '(':
                return TBoolS(value)
            else:
                return TBoolI(value)
        raise Exception("ERROR: Could not parse temporal boolean value")

    @staticmethod
    def write(value):
        if not isinstance(value, TBool):
            raise ValueError('TBool value must subclass TBool class')
        return value.__str__().strip("'")


class TBoolInst(TemporalInst, TBool):
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

    """
    It is not possible to call super().__init__(value, time) since bool('False') == True
    and eval('False') == False. Furthermore eval('false') gives an error
    """
    def __init__(self, value, time=None):
        TemporalInst.BaseClass = bool
        if time is None:
            # Constructor with a single argument of type string
            if isinstance(value, str):
                couple = parse_temporalinst(value, 0)
                value = couple[2][0]
                time = couple[2][1]
            # Constructor with a single argument of type tuple or list
            elif isinstance(value, (tuple, list)):
                value, time = value
            else:
                raise Exception("ERROR: Could not parse temporal instant value")
        # Now both value and time are not None
        assert(isinstance(value, (str, bool))), "ERROR: Invalid value argument"
        assert(isinstance(time, (str, datetime))), "ERROR: Invalid time argument"
        if isinstance(value, str):
            if value.lower() == 'true' or value.lower() == 't':
                self._value = True
            elif value.lower() == 'false' or value.lower() == 'f':
                self._value = False
            else:
                raise Exception("ERROR: Could not parse temporal instant value")
        else:
            self._value =  value
        self._time = parse(time) if isinstance(time, str) else time


class TBoolI(TemporalI, TBool):
    """
    Class for representing temporal Booleans of instant set duration.

    ``TBoolI`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TBoolI('AA@2019-09-01')

    Another possibility is to give a tuple or list of arguments,
    which can be instances of ``str`` or ``TBoolInst``.

        >>> TBoolI('AA@2019-09-01 00:00:00+01', 'BB@2019-09-02 00:00:00+01', 'AA@2019-09-03 00:00:00+01')
        >>> TBoolI(TBoolInst('AA@2019-09-01 00:00:00+01'), TBoolInst('BB@2019-09-02 00:00:00+01'), TBoolInst('AA@2019-09-03 00:00:00+01'))
        >>> TBoolI(['AA@2019-09-01 00:00:00+01', 'BB@2019-09-02 00:00:00+01', 'AA@2019-09-03 00:00:00+01'])
        >>> TBoolI([TBoolInst('AA@2019-09-01 00:00:00+01'), TBoolInst('BB@2019-09-02 00:00:00+01'), TBoolInst('AA@2019-09-03 00:00:00+01')])

    """

    def __init__(self,  *argv):
        TemporalI.BaseClass = bool
        TemporalI.ComponentClass = TBoolInst
        super().__init__(*argv)


class TBoolSeq(TemporalSeq, TBool):
    """
    Class for representing temporal Booleans of sequence duration.

    ``TBoolSeq`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TBoolSeq('[true@2019-09-01 00:00:00+01, false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]')

    Another possibility is to give the arguments as follows.

    * ``instantList`` is the list of composing instants, which can be instances of
      ``str`` or ``TBoolInst``,
    * ``lower_inc`` and ``upper_inc`` are instances of ``bool`` specifying
      whether the bounds are inclusive or not. By default ``lower_inc``
      is ``True`` and ``upper_inc`` is ``False``.

    Some examples are given next.

        >>> TBoolSeq(['true@2019-09-01 00:00:00+01', 'false@2019-09-02 00:00:00+01', 'true@2019-09-03 00:00:00+01'])
        >>> TBoolSeq(TBoolInst('true@2019-09-01 00:00:00+01'), TBoolInst('false@2019-09-02 00:00:00+01'), TBoolInst('true@2019-09-03 00:00:00+01')])
        >>> TBoolSeq(['true@2019-09-01 00:00:00+01', 'false@2019-09-02 00:00:00+01', 'true@2019-09-03 00:00:00+01'], True, True)
        >>> TBoolSeq([TBoolInst('true@2019-09-01 00:00:00+01'), TBoolInst('false@2019-09-02 00:00:00+01'), TBoolInst('true@2019-09-03 00:00:00+01')], True, True)

    """

    def __init__(self, instantList, lower_inc=None, upper_inc=None):
        TemporalSeq.BaseClass = bool
        TemporalSeq.BaseClassDiscrete = True
        TemporalSeq.ComponentClass = TBoolInst
        self._interp = 'Stepwise'
        super().__init__(instantList, lower_inc, upper_inc)

    @classmethod
    @property
    def interpolation(self):
        """
        Interpolation of the temporal value, that is, ``'Stepwise'``.
        """
        return 'Stepwise'


class TBoolS(TemporalS, TBool):
    """
    Class for representing temporal Booleans of sequence set duration.

    ``TBoolS`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TBoolS('{[true@2019-09-01 00:00:00+01], [false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]}')

    Another possibility is to give the list of composing sequences, which
    can be instances of ``str`` or ``TBoolSeq``.

        >>> TBoolS(['[true@2019-09-01 00:00:00+01]', '[false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]'])
        >>> TBoolS([TBoolSeq('[true@2019-09-01 00:00:00+01]'), TBoolSeq('[false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]')])
        >>> TBoolS([TBoolSeq('[true@2019-09-01 00:00:00+01]'), TBoolSeq('[false@2019-09-02 00:00:00+01, true@2019-09-03 00:00:00+01]')])

    """

    def __init__(self, sequenceList):
        TemporalS.BaseClass = bool
        TemporalS.BaseClassDiscrete = True
        TemporalS.ComponentClass = TBoolSeq
        self._interp = 'Stepwise'
        super().__init__(sequenceList)

    @classmethod
    @property
    def interpolation(self):
        """
        Interpolation of the temporal value, that is, ``'Stepwise'``.
        """
        return 'Stepwise'

