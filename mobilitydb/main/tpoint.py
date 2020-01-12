import re
from datetime import datetime
from dateutil.parser import parse
from postgis import Geometry, Point, MultiPoint, LineString, GeometryCollection, MultiLineString
from mobilitydb.temporal import Temporal, TemporalInst, TemporalI, TemporalSeq, TemporalS
from mobilitydb.temporal.temporal_parser import parse_temporalinst, parse_temporali, parse_temporalseq, parse_temporals


# Add method to Point to make the class hashable
def __hash__(self):
    return hash(self.values())

setattr(Point, '__hash__', __hash__)


class TPointInst(TemporalInst):
    """
    Abstract class for representing temporal points of instant duration.
    """

    def __init__(self, value, time=None, srid=None):
        if time is None:
            # Constructor with a single argument of type string
            if isinstance(value, str):
                # If srid is given
                if re.match(r'^(SRID|srid)\s*=\s*\d+\s*(;|,)\s*', value):
                    #Get the srid and remove the "srid=xxx;" prefix
                    srid_str = int(re.search(r'(\d+)', value).group())
                    if srid is not None and srid_str != srid:
                        raise Exception(f"ERROR: SRID mismatch: {srid_str} vs {srid}")
                    srid = srid_str
                    value = re.sub(r'^(SRID|srid)\s*=\s*\d+\s*(;|,)\s*', '', value)
                else:
                    srid = 0
                #Parse without the eventual "srid=xxx;" prefix
                couple = parse_temporalinst(value, 0)
                value = couple[2][0]
                time = couple[2][1]
            # Constructor with a single argument of type tuple or list
            elif isinstance(value, (tuple, list)):
                value, time, *extra = value
                if extra:
                    srid, *extra = extra
                else:
                    srid = 0
            else:
                raise Exception("ERROR: Could not parse temporal instant value")
        if srid is None:
            srid = 0
        # Now value, time, and srid are not None
        assert(isinstance(value, (str, Point))), "ERROR: Invalid value argument"
        assert(isinstance(time, (str, datetime))), "ERROR: Invalid time argument"
        assert(isinstance(srid, (str, int))), "ERROR: Invalid SRID"
        if isinstance(value, str):
            if '(' in value and ')' in value:
                idx1 = value.find('(')
                idx2 = value.find(')')
                coords = (value[idx1 + 1:idx2]).split(' ')
                self._value = Point(coords, srid=srid)
            else:
                self._value = Geometry.from_ewkb(value)
        else:
            self._value = value
        self._time = parse(time) if isinstance(time, str) else time
        # Verify validity of the resulting instance
        self._valid()

    def _valid(self):
        if self._value.m is not None:
            raise Exception("ERROR: The points composing a temporal point cannot have M dimension")

    @property
    def getValues(self):
        """
        Geometry representing the values taken by the temporal value.
        """
        return self._value


class TPointI(TemporalI):
    """
    Abstract class for representing temporal points of instant set duration.
    """

    def __init__(self,  *argv, srid=None):
        self._instantList = []
        # Constructor with a single argument of type string
        if len(argv) == 1 and isinstance(argv[0], str):
            # If srid is given
            if re.match(r'^(SRID|srid)\s*=\s*\d+\s*(;|,)\s*', argv[0]):
                # Get the srid and remove the "srid=xxx;" prefix
                srid_str = int(re.search(r'(\d+)', argv[0]).group())
                if srid is not None and srid_str != srid:
                    raise Exception(f"ERROR: SRID mismatch: {srid_str} vs {srid}")
                srid = srid_str
                instantList = re.sub(r'^(SRID|srid)\s*=\s*\d+\s*(;|,)\s*', '', argv[0])
            else:
                instantList = argv[0]
            # Parse without the eventual "srid=xxx;" prefix
            elements = parse_temporali(instantList, 0)
            for inst in elements[2]:
                self._instantList.append(TemporalI.ComponentClass(inst[0], inst[1], srid=srid))
        # Constructor with a single argument of type list
        elif len(argv) == 1 and isinstance(argv[0], list):
            # List of strings representing instant values
            if all(isinstance(arg, str) for arg in argv[0]):
                for arg in argv[0]:
                    self._instantList.append(TemporalI.ComponentClass(arg))
            # List of instant values
            elif all(isinstance(arg, TemporalI.ComponentClass) for arg in argv[0]):
                for arg in argv[0]:
                    self._instantList.append(arg)
            else:
                raise Exception("ERROR: Could not parse temporal instant set value")
        # Constructor with multiple arguments
        else:
            # Arguments are of type string
            if all(isinstance(arg, str) for arg in argv):
                for arg in argv:
                    self._instantList.append(TemporalI.ComponentClass(arg))
            # Arguments are of type instant
            elif all(isinstance(arg, TemporalI.ComponentClass) for arg in argv):
                for arg in argv:
                    self._instantList.append(arg)
            else:
                raise Exception("ERROR: Could not parse temporal instant set value")
        # Verify validity of the resulting instance
        self._valid()

    def _valid(self):
        super()._valid()
        if any((x._value.z is None and y._value.z is not None) or (x._value.z is not None and y._value.z is None) \
                for x, y in zip(self._instantList, self._instantList[1:])):
            raise Exception("ERROR: The points composing a temporal point must be of the same dimensionality")
        if any(x._value.m is not None for x in self._instantList):
            raise Exception("ERROR: The points composing a temporal point cannot have M dimension")
        if any(x.srid != y.srid for x, y in zip(self._instantList, self._instantList[1:])):
            raise Exception("ERROR: The points composing a temporal point must have the same SRID")

    @property
    def getValues(self):
        """
        Geometry representing the values taken by the temporal value.
        """
        values = super().getValues
        return MultiPoint(values)


class TPointSeq(TemporalSeq):
    """
    Abstract class for representing temporal points of sequence duration.
    """

    def __init__(self, instantList, lower_inc=None, upper_inc=None, interp=None, srid=None):
        assert (isinstance(lower_inc, (bool, type(None)))), "ERROR: Invalid lower bound flag"
        assert (isinstance(upper_inc, (bool, type(None)))), "ERROR: Invalid upper bound flag"
        assert (isinstance(interp, (str, type(None)))), "ERROR: Invalid interpolation"
        if isinstance(interp, str):
            assert (interp == 'Linear' or interp == 'Stepwise'), "ERROR: Invalid interpolation"
        self._instantList = []
        # Constructor with a first argument of type string and optional arguments for the bounds and interpolation
        if isinstance(instantList, str):
            # If srid is given
            if re.match(r'^(SRID|srid)\s*=\s*\d+\s*(;|,)\s*', instantList):
                # Get the srid and remove the "srid=xxx;" prefix
                srid_str = int(re.search(r'(\d+)', instantList).group())
                if srid is not None and srid_str != srid:
                    raise Exception(f"ERROR: SRID mismatch: {srid_str} vs {srid}")
                srid = srid_str
                instantList = re.sub(r'^(SRID|srid)\s*=\s*\d+\s*(;|,)\s*', '', instantList)
            # Parse without the eventual "srid=xxx;" prefix
            elements = parse_temporalseq(instantList, 0)
            for inst in elements[2][0]:
                self._instantList.append(TemporalSeq.ComponentClass(inst[0], inst[1], srid=srid))
            self._lower_inc = elements[2][1]
            self._upper_inc = elements[2][2]
            # Set interpolation with the argument or the flag from the string if given
            if interp is not None:
                self._interp = interp
            else:
                if self.__class__.BaseClassDiscrete:
                    self._interp = 'Stepwise'
                else:
                    self._interp = elements[2][3] if elements[2][3] is not None else 'Linear'
        # Constructor with a first argument of type list and optional arguments for the bounds and interpolation
        elif isinstance(instantList, list):
            # List of strings representing instant values
            if all(isinstance(arg, str) for arg in instantList):
                for arg in instantList:
                    self._instantList.append(TemporalSeq.ComponentClass(arg))
            # List of instant values
            elif all(isinstance(arg, TemporalSeq.ComponentClass) for arg in instantList):
                for arg in instantList:
                    self._instantList.append(arg)
            else:
                raise Exception("ERROR: Could not parse temporal sequence value")
            self._lower_inc = lower_inc if lower_inc is not None else True
            self._upper_inc = upper_inc if upper_inc is not None else False
            # Set the interpolation
            if interp is not None:
                self._interp = interp
            else:
                self._interp = 'Stepwise' if self.__class__.BaseClassDiscrete else 'Linear'
        else:
            raise Exception("ERROR: Could not parse temporal sequence value")
        # Verify validity of the resulting instance
        self._valid()

    def _valid(self):
        super()._valid()
        if any((x._value.z is None and y._value.z is not None) or (x._value.z is not None and y._value.z is None) \
                for x, y in zip(self._instantList, self._instantList[1:])):
            raise Exception("ERROR: The points composing a temporal point must be of the same dimensionality")
        if any(x._value.m is not None for x in self._instantList):
            raise Exception("ERROR: The points composing a temporal point cannot have M dimension")
        if any(x.srid != y.srid for x, y in zip(self._instantList, self._instantList[1:])):
            raise Exception("ERROR: The points composing a temporal point must have the same SRID")


    @property
    def interpolation(self):
        """
        Interpolation of the temporal value, which is either ``'Linear'`` or ``'Stepwise'``.
        """
        return self._interp

    @property
    def getValues(self):
        """
        Geometry representing the values taken by the temporal value.
        """
        values = [inst._value for inst in self._instantList]
        result = values[0] if len(values) == 1 else LineString(values)
        return result


class TPointS(TemporalS):
    """
    Abstract class for representing temporal points of sequence set duration.
    """

    def __init__(self, sequenceList, interp=None, srid=None):
        assert (isinstance(interp, (str, type(None)))), "ERROR: Invalid interpolation"
        if isinstance(interp, str) and interp is None:
            assert (interp == 'Linear' or interp == 'Stepwise'), "ERROR: Invalid interpolation"
        self._sequenceList = []
        # Constructor with a single argument of type string
        if isinstance(sequenceList, str):
            # If srid is given
            if re.match(r'^(SRID|srid)\s*=\s*\d+\s*(;|,)\s*', sequenceList):
                # Get the srid and remove the "srid=xxx;" prefix
                srid_str = int(re.search(r'(\d+)', sequenceList).group())
                if srid is not None and srid_str != srid:
                    raise Exception(f"ERROR: SRID mismatch: {srid_str} vs {srid}")
                srid = srid_str
                sequenceList = re.sub(r'^(SRID|srid)\s*=\s*\d+\s*(;|,)\s*', '', sequenceList)
            # Parse without the eventual "srid=xxx;" prefix
            elements = parse_temporals(sequenceList, 0)
            seqList = []
            for seq in elements[2][0]:
                instList = []
                for inst in seq[0]:
                    instList.append(TemporalS.ComponentClass.ComponentClass(inst[0], inst[1], srid=srid))
                if self.__class__.BaseClassDiscrete:
                    seqList.append(TemporalS.ComponentClass(instList, seq[1], seq[2]))
                else:
                    seqList.append(TemporalS.ComponentClass(instList, seq[1], seq[2], elements[2][1], srid=srid))
            self._sequenceList = seqList
            # Set interpolation with the argument or the flag from the string if given
            if interp is not None:
                self._interp = interp
            else:
                if self.__class__.BaseClassDiscrete:
                    self._interp = 'Stepwise'
                else:
                    self._interp = elements[2][1] if elements[2][1] is not None else 'Linear'
        # Constructor with a single argument of type list
        elif isinstance(sequenceList, list):
            # List of strings representing periods
            if all(isinstance(sequence, str) for sequence in sequenceList):
                for sequence in sequenceList:
                    self._sequenceList.append(self.__class__.ComponentClass(sequence))
            # List of periods
            elif all(isinstance(sequence, self.__class__.ComponentClass) for sequence in sequenceList):
                for sequence in sequenceList:
                    self._sequenceList.append(sequence)
            else:
                raise Exception("ERROR: Could not parse temporal sequence set value")
            # Set the interpolation
            if interp is not None:
                self._interp = interp
            else:
                self._interp = 'Stepwise' if self.__class__.BaseClassDiscrete else 'Linear'
        else:
            raise Exception("ERROR: Could not parse temporal sequence set value")
        # Verify validity of the resulting instance
        self._valid()

    def _valid(self):
        super()._valid()
        if any((x.hasz is None and y.hasz is not None) or (x.hasz is not None and y.hasz is None) \
                for x, y in zip(self._sequenceList, self._sequenceList[1:])):
            raise Exception("ERROR: The points composing a temporal point must be of the same dimensionality")
        if any(x.srid != y.srid for x, y in zip(self._sequenceList, self._sequenceList[1:])):
            raise Exception("ERROR: The points composing a temporal point must have the same SRID")

    @property
    def interpolation(self):
        """
        Interpolation of the temporal value, which is either ``'Linear'`` or ``'Stepwise'``.
        """
        return self._interp

    @property
    def getValues(self):
        """
        Geometry representing the values taken by the temporal value.
        """
        values = [seq.getValues for seq in self._sequenceList]
        points = [geo for geo in values if isinstance(geo, Point)]
        lines = [geo for geo in values if isinstance(geo, LineString)]
        if len(points) != 0 and len(points) != 0:
            return GeometryCollection(points + lines)
        if len(points) != 0 and len(points) == 0:
            return MultiPoint(points)
        if len(points) == 0 and len(points) != 0:
            return MultiLineString(lines)


class TGeomPoint(Temporal):
    """
    Abstract class for representing temporal geometric or geographic points of any duration.
    """

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        if value.startswith('Interp=Stepwise;'):
            value1 = value.replace('Interp=Stepwise;', '')
            if value1[0] == '{':
                return TGeomPointS(value)
            else:
                return TGeomPointSeq(value)
        elif value[0] != '{' and value[0] != '[' and value[0] != '(':
            return TGeomPointInst(value)
        elif value[0] == '[' or value[0] == '(':
            return TGeomPointSeq(value)
        elif value[0] == '{':
            if value[1] == '[' or value[1] == '(':
                return TGeomPointS(value)
            else:
                return TGeomPointI(value)
        raise Exception("ERROR: Could not parse temporal point value")

    @staticmethod
    def write(value):
        if not isinstance(value, TGeomPoint):
            raise ValueError('Value must an instance of a subclass of TGeomPoint')
        return value.__str__().strip("'")

    @property
    def hasz(self):
        """
        Does the temporal point has Z dimension?
        """
        return self.startValue.z is not None

    @property
    def srid(self):
        """
        Returns the SRID.
        """
        result = self.startValue.srid if hasattr(self.startValue, "srid") else None
        return result


class TGeogPoint(Temporal):
    """
    Abstract class for representing temporal geographic points of any duration.
    """

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        if value.startswith('Interp=Stepwise;'):
            value1 = value.replace('Interp=Stepwise;', '')
            if value1[0] == '{':
                return TGeogPointS(value)
            else:
                return TGeogPointSeq(value)
        elif value[0] != '{' and value[0] != '[' and value[0] != '(':
            return TGeogPointInst(value)
        elif value[0] == '[' or value[0] == '(':
            return TGeogPointSeq(value)
        elif value[0] == '{':
            if value[1] == '[' or value[1] == '(':
                return TGeogPointS(value)
            else:
                return TGeogPointI(value)
        raise Exception("ERROR: Could not parse temporal point value")

    @staticmethod
    def write(value):
        if not isinstance(value, TGeogPoint):
            raise ValueError('Value must an instance of a subclass of TGeogPoint')
        return value.__str__().strip("'")

    @property
    def hasz(self):
        """
        Does the temporal point has Z dimension?
        """
        return self.startValue.z is not None

    @property
    def srid(self):
        """
        Returns the SRID.
        """
        result = self.startValue.srid if hasattr(self.startValue, "srid") else None
        return result


class TGeomPointInst(TPointInst, TGeomPoint):
    """
    Class for representing temporal geometric points of instant duration.

    ``TGeomPointInst`` objects can be created with a single argument of type
    string as in MobilityDB.

        >>> TGeomPointInst('Point(10.0 10.0)@2019-09-01')
        >>> TGeomPointInst('SRID=4326,Point(10.0 10.0)@2019-09-01')

    Another possibility is to give the ``value`` and the ``time`` arguments,
    which can be instances of ``str``, ``Point`` or ``datetime``.
    Additionally, the SRID can be specified, it will be 0 by default if not
    given.

        >>> TGeomPointInst('Point(10.0 10.0)', '2019-09-08 00:00:00+01', 4326)
        >>> TGeomPointInst(['Point(10.0 10.0)', '2019-09-08 00:00:00+01', 4326])
        >>> TGeomPointInst(Point(10.0, 10.0), parse('2019-09-08 00:00:00+01'), 4326)
        >>> TGeomPointInst([Point(10.0, 10.0), parse('2019-09-08 00:00:00+01'), 4326])

    """

    def __init__(self, value, time=None, srid=None):
        TemporalInst.BaseClass = Point
        super().__init__(value, time, srid)


class TGeogPointInst(TPointInst, TGeogPoint):
    """
    Class for representing temporal geographic points of instant duration.

    ``TGeogPointInst`` objects can be created with a single argument of type
    string as in MobilityDB.

        >>> TGeogPointInst('Point(10.0 10.0)@2019-09-01')

    Another possibility is to give the ``value`` and the ``time`` arguments,
    which can be instances of ``str``, ``Point`` or ``datetime``.
    Additionally, the SRID can be specified, it will be 0 by default if not
    given.

        >>> TGeogPointInst('Point(10.0 10.0)', '2019-09-08 00:00:00+01')
        >>> TGeogPointInst(['Point(10.0 10.0)', '2019-09-08 00:00:00+01'])
        >>> TGeogPointInst(Point(10.0, 10.0), parse('2019-09-08 00:00:00+01'))
        >>> TGeogPointInst([Point(10.0, 10.0), parse('2019-09-08 00:00:00+01')])

    """

    def __init__(self, value, time=None, srid=None):
        TemporalInst.BaseClass = Point
        super().__init__(value, time, srid)


class TGeomPointI(TPointI, TGeomPoint):
    """
    Class for representing temporal geometric points of instant set duration.

    ``TGeomPointI`` objects can be created with a single argument of type
    string as in MobilityDB.

        >>> TGeomPointI('Point(10.0 10.0)@2019-09-01')

    Another possibility is to give a tuple or list of arguments specifying
    the composing instants, which can be instances of ``str`` or
    ``TGeomPointInst``.

        >>> TGeomPointI('Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01', 'Point(10.0 10.0)@2019-09-03 00:00:00+01')
        >>> TGeomPointI(TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'), TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'), TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01'))
        >>> TGeomPointI(['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01', 'Point(10.0 10.0)@2019-09-03 00:00:00+01'])
        >>> TGeomPointI([TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'), TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'), TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')])

    """

    def __init__(self,  *argv, **kwargs):
        TemporalI.BaseClass = Point
        TemporalI.ComponentClass = TGeomPointInst
        super().__init__(*argv, **kwargs)


class TGeogPointI(TPointI, TGeogPoint):
    """
    Class for representing temporal geometric points of instant set duration.

    ``TGeogPointI`` objects can be created with a single argument of type
    string as in MobilityDB.

        >>> TGeogPointI('Point(10.0 10.0)@2019-09-01')

    Another possibility is to give a tuple or list of arguments specifying
    the composing instants, which can be instances of ``str`` or
    ``TGeogPointInst``.

        >>> TGeogPointI('Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01', 'Point(10.0 10.0)@2019-09-03 00:00:00+01')
        >>> TGeogPointI(TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'), TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'), TGeogPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01'))
        >>> TGeogPointI(['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01', 'Point(10.0 10.0)@2019-09-03 00:00:00+01'])
        >>> TGeogPointI([TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'), TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'), TGeogPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')])

    """

    def __init__(self,  *argv, **kwargs):
        TemporalI.BaseClass = Point
        TemporalI.ComponentClass = TGeogPointInst
        super().__init__(*argv, **kwargs)


class TGeomPointSeq(TPointSeq, TGeomPoint):
    """
    Class for representing temporal geometric points of sequence duration.

    ``TGeomPointSeq`` objects can be created with a single argument of type
    string as in MobilityDB.

        >>> TGeomPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')
        >>> TGeomPointSeq('Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')

    Another possibility is to give the arguments as follows:

    * ``instantList`` is the list of composing instants, which can be instances
      of ``str`` or ``TGeogPointInst``,
    * ``lower_inc`` and ``upper_inc`` are instances of ``bool`` specifying
      whether the bounds are inclusive or not,  where by default '`lower_inc``
      is ``True`` and ``upper_inc`` is ``False``,
    * ``interp`` which is either ``'Linear'`` or ``'Stepwise'``, the former
      being the default, and
    * ``srid`` is an integer specifiying the SRID

    Some examples are shown next.

        >>> TGeomPointSeq(['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01', 'Point(10.0 10.0)@2019-09-03 00:00:00+01'])
        >>> TGeomPointSeq([TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'), TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'), TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')])
        >>> TGeomPointSeq(['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01', 'Point(10.0 10.0)@2019-09-03 00:00:00+01'], True, True, 'Stepwise')
        >>> TGeomPointSeq([TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'), TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'), TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')], True, True, 'Stepwise')

    """

    def __init__(self, instantList, lower_inc=None, upper_inc=None, interp=None, srid=None):
        TemporalSeq.BaseClass = Point
        TemporalSeq.BaseClassDiscrete = False
        TemporalSeq.ComponentClass = TGeomPointInst
        super().__init__(instantList, lower_inc, upper_inc, interp, srid)


class TGeogPointSeq(TPointSeq, TGeogPoint):
    """
    Class for representing temporal geographic points of sequence duration.

    ``TGeogPointSeq`` objects can be created with a single argument of type
    string as in MobilityDB.

        >>> TGeogPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')
        >>> TGeogPointSeq('Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')

    Another possibility is to give the arguments as follows:

    * ``instantList`` is the list of composing instants, which can be instances
      of ``str`` or ``TGeogPointInst``,
    * ``lower_inc`` and ``upper_inc`` are instances of ``bool`` specifying
      whether the bounds are includive or not,  where by default '`lower_inc``
      is ``True`` and ``upper_inc`` is ``False``, and
    * ``interp`` which is either ``'Linear'`` or ``'Stepwise'``, the former
      being the default.
    * ``srid`` is an integer specifiying the SRID

    Some examples are shown next.

        >>> TGeogPointSeq(['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01', 'Point(10.0 10.0)@2019-09-03 00:00:00+01'])
        >>> TGeogPointSeq([TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'), TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'), TGeogPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')])
        >>> TGeogPointSeq(['Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01', 'Point(10.0 10.0)@2019-09-03 00:00:00+01'], True, True, 'Stepwise')
        >>> TGeogPointSeq([TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'), TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'), TGeogPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')], True, True, 'Stepwise')

    """

    def __init__(self, instantList, lower_inc=None, upper_inc=None, interp=None, srid=None):
        TemporalSeq.BaseClass = Point
        TemporalSeq.BaseClassDiscrete = False
        TemporalSeq.ComponentClass = TGeogPointInst
        super().__init__(instantList, lower_inc, upper_inc, interp, srid)


class TGeomPointS(TPointS, TGeomPoint):
    """
    Class for representing temporal geometric points of sequence duration.

    ``TGeomPointS`` objects can be created with a single argument of type
    string as in MobilityDB.

        >>> TGeomPointS('{[Point(10.0 10.0)@2019-09-01 00:00:00+01], [Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]}')
        >>> TGeomPointS('Interp=Stepwise;{[Point(10.0 10.0)@2019-09-01 00:00:00+01], [Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]}')

    Another possibility is to give the arguments as follows:

    * ``sequenceList`` is the list of composing sequences, which can be instances
      of ``str`` or ``TGeomPointSeq``,
    * ``interp`` can be ``'Linear'`` or ``'Stepwise'``, the former being
      the default, and
    * ``srid`` is an integer specifiying the SRID, if will be 0 by default if
      not given.

    Some examples are shown next.

        >>> TGeomPointS(['[Point(10.0 10.0)@2019-09-01 00:00:00+01]', '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'])
        >>> TGeomPointS(['[Point(10.0 10.0)@2019-09-01 00:00:00+01]', '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'], 'Linear')
        >>> TGeomPointS(['Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]', 'Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'], 'Stepwise')
        >>> TGeomPointS([TGeomPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'), TGeomPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')])
        >>> TGeomPointS([TGeomPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),  TGeomPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')], 'Linear')
        >>> TGeomPointS([TGeomPointSeq('Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]'), TGeomPointSeq('Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')], 'Stepwise')

    """

    def __init__(self, sequenceList, interp=None, srid=None):
        TemporalS.BaseClass = Point
        TemporalS.BaseClassDiscrete = False
        TemporalS.ComponentClass = TGeomPointSeq
        super().__init__(sequenceList, interp, srid)


class TGeogPointS(TPointS, TGeogPoint):
    """
    Class for representing temporal geographic points of sequence duration.

    ``TGeogPointS`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TGeogPointS('{[Point(10.0 10.0)@2019-09-01 00:00:00+01], [Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]}')
        >>> TGeogPointS('Interp=Stepwise;{[Point(10.0 10.0)@2019-09-01 00:00:00+01], [Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]}')

    Another possibility is to give the arguments as follows:

    * ``sequenceList`` is the list of composing sequences, which can be instances
      of ``str`` or ``TGeogPointSeq``,
    * ``interp`` can be ``'Linear'`` or ``'Stepwise'``, the former being
      the default, and
    * ``srid`` is an integer specifiying the SRID, if will be 0 by default if
      not given.

    Some examples are shown next.

        >>> TGeogPointS(['[Point(10.0 10.0)@2019-09-01 00:00:00+01]', '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'])
        >>> TGeogPointS(['[Point(10.0 10.0)@2019-09-01 00:00:00+01]', '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'], 'Linear')
        >>> TGeogPointS(['Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]', 'Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'], 'Stepwise')
        >>> TGeogPointS([TGeogPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'), TGeogPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')])
        >>> TGeogPointS([TGeogPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'),  TGeogPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')], 'Linear')
        >>> TGeogPointS([TGeogPointSeq('Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]'), TGeogPointSeq('Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')], 'Stepwise')

    """

    def __init__(self, sequenceList, interp=None, srid=None):
        TemporalS.BaseClass = Point
        TemporalS.BaseClassDiscrete = False
        TemporalS.ComponentClass = TGeogPointSeq
        super().__init__(sequenceList, interp, srid)
