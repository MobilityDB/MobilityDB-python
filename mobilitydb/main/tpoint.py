import re
from datetime import datetime
from dateutil.parser import parse

from postgis import (
    Geometry,
    Point,
    MultiPoint,
    LineString,
    GeometryCollection,
    MultiLineString,
)
from pymeos import GeomPoint
from pymeos.range import RangeGeom
from pymeos.temporal import (
    Interpolation,
    TGeomPointInst as _TGeomPointInst,
    TGeomPointInstSet as _TGeomPointInstSet,
    TGeomPointSeq as _TGeomPointSeq,
    TGeomPointSeqSet as _TGeomPointSeqSet,
)

from mobilitydb.temporal import Temporal


# Add method to Point to make the class hashable
def __hash__(self):
    return hash(self.values())


setattr(Point, "__hash__", __hash__)


def to_coords(geom):
    """
    Converts a MEOS Geometry object to a tuple of (x, y) values
    """
    return (geom.x, geom.y)


class TPointInst(_TGeomPointInst):
    """
    Abstract class for representing temporal points of instant duration.
    """

    def __init__(self, value, time=None, srid=None):
        if srid is None:
            srid = self.default_srid

        if time is None:
            # Constructor with a single argument of type string
            if isinstance(value, str):
                super().__init__(value, srid)
            # Constructor with a single argument of type tuple or list
            elif isinstance(value, (tuple, list)):
                value, time, *extra = value
                if extra:
                    srid, *extra = extra
                super().__init__(value, time, srid)
            else:
                raise Exception("ERROR: Could not parse temporal instant value")
        else:
            super().__init__(value, time, srid)

    @property
    def getValues(self):
        """
        Geometry representing the values taken by the temporal value.
        """
        return self.getValue


class TPointInstSet(_TGeomPointInstSet):
    """
    Abstract class for representing temporal points of instant set duration.
    """

    BaseClass = GeomPoint

    def __init__(self, *argv, srid=None):
        _instants = set()

        if srid is None:
            srid = self.default_srid

        super().__init__(argv[0], srid)

    @property
    def getValues(self):
        """
        Geometry representing the values taken by the temporal value.
        """
        values = sorted([to_coords(v.getValue) for v in self.instants])
        return MultiPoint(values)


class TPointSeq(_TGeomPointSeq):
    """
    Abstract class for representing temporal points of sequence duration.
    """

    BaseClass = GeomPoint
    BaseClassDiscrete = False

    def __init__(
        self, instants, lower_inc=None, upper_inc=None, srid=None, interp=None
    ):
        if srid is None:
            srid = self.default_srid
        if interp is None:
            interp = self.default_interp
        interp = Interpolation.__members__.get(interp)

        if isinstance(instants, str):
            super().__init__(instants, srid)
        elif lower_inc is None:
            super().__init__(instants, True, False, srid, interp)
        super().__init__(instants, lower_inc, upper_inc, srid, interp)

    @property
    def getValues(self):
        """
        Geometry representing the values taken by the temporal value.
        """
        values = [to_coords(inst.getValue) for inst in sorted(self.instants)]
        result = Point(values[0]) if len(values) == 1 else LineString(values)
        return result


class TPointSeqSet(_TGeomPointSeqSet):
    """
    Abstract class for representing temporal points of sequence set duration.
    """

    BaseClass = GeomPoint
    BaseClassDiscrete = False

    def __init__(self, sequences, srid=None, interp=None):
        if srid is None:
            srid = self.default_srid
        if interp is None:
            interp = self.default_interp
        interp = Interpolation.__members__.get(interp)

        if isinstance(sequences, str) or interp is None:
            super().__init__(sequences, srid)
        else:
            super().__init__(sequences, srid, interp)

    @property
    def getValues(self):
        """
        Geometry representing the values taken by the temporal value.
        """

        def seq_to_geom(seq):
            values = [to_coords(inst.getValue) for inst in sorted(seq.instants)]
            return Point(values[0]) if len(values) == 1 else LineString(values)

        values = [seq_to_geom(seq) for seq in self.sequences]
        points = [geo for geo in values if isinstance(geo, Point)]
        lines = [geo for geo in values if isinstance(geo, LineString)]
        if len(points) != 0 and len(lines) != 0:
            return GeometryCollection(points + lines)
        if len(points) != 0 and len(lines) == 0:
            return MultiPoint(points)
        if len(points) == 0 and len(lines) != 0:
            return MultiLineString(lines)


class TGeomPoint(Temporal):
    """
    Abstract class for representing temporal geometric or geographic points of any duration.
    """

    pymeos_range_type = RangeGeom
    default_srid = 0
    default_interp = "Linear"

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        if value.startswith("Interp=Stepwise;"):
            value1 = value.replace("Interp=Stepwise;", "")
            if value1[0] == "{":
                return TGeomPointSeqSet(value)
            else:
                return TGeomPointSeq(value)
        elif value[0] != "{" and value[0] != "[" and value[0] != "(":
            return TGeomPointInst(value)
        elif value[0] == "[" or value[0] == "(":
            return TGeomPointSeq(value)
        elif value[0] == "{":
            if value[1] == "[" or value[1] == "(":
                return TGeomPointSeqSet(value)
            else:
                return TGeomPointInstSet(value)
        raise Exception("ERROR: Could not parse temporal point value")

    @staticmethod
    def write(value):
        if not isinstance(value, TGeomPoint):
            raise ValueError("Value must an instance of a subclass of TGeomPoint")
        return value.__str__()

    @property
    def hasz(self):
        """
        Does the temporal point has Z dimension?
        """
        return self.startValue.z is not None


class TGeogPoint(Temporal):
    """
    Abstract class for representing temporal geographic points of any duration.
    """

    pymeos_range_type = RangeGeom
    default_srid = 4326
    default_interp = "Linear"

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        if value.startswith("Interp=Stepwise;"):
            value1 = value.replace("Interp=Stepwise;", "")
            if value1[0] == "{":
                return TGeogPointSeqSet(value)
            else:
                return TGeogPointSeq(value)
        elif value[0] != "{" and value[0] != "[" and value[0] != "(":
            return TGeogPointInst(value)
        elif value[0] == "[" or value[0] == "(":
            return TGeogPointSeq(value)
        elif value[0] == "{":
            if value[1] == "[" or value[1] == "(":
                return TGeogPointSeqSet(value)
            else:
                return TGeogPointInstSet(value)
        raise Exception("ERROR: Could not parse temporal point value")

    @staticmethod
    def write(value):
        if not isinstance(value, TGeogPoint):
            raise ValueError("Value must an instance of a subclass of TGeogPoint")
        return value.__str__()

    @property
    def hasz(self):
        """
        Does the temporal point has Z dimension?
        """
        return self.startValue.z is not None


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

    pass


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

    pass


class TGeomPointInstSet(TPointInstSet, TGeomPoint):
    """
    Class for representing temporal geometric points of instant set duration.

    ``TGeomPointInstSet`` objects can be created with a single argument of type
    string as in MobilityDB.

        >>> TGeomPointInstSet('Point(10.0 10.0)@2019-09-01')

    Another possibility is to give a set of arguments specifying
    the composing instants, which can be instances of ``str`` or
    ``TGeomPointInst``.

        >>> TGeomPointInstSet({'Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01', 'Point(10.0 10.0)@2019-09-03 00:00:00+01'})
        >>> TGeomPointInstSet({TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'), TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'), TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')})
    """

    ComponentClass = TGeomPointInst


class TGeogPointInstSet(TPointInstSet, TGeogPoint):
    """
    Class for representing temporal geometric points of instant set duration.

    ``TGeogPointInstSet`` objects can be created with a single argument of type
    string as in MobilityDB.

        >>> TGeogPointInstSet('Point(10.0 10.0)@2019-09-01')

    Another possibility is to give a set of arguments specifying
    the composing instants, which can be instances of ``str`` or
    ``TGeogPointInst``.

        >>> TGeogPointInstSet({'Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01', 'Point(10.0 10.0)@2019-09-03 00:00:00+01'})
        >>> TGeogPointInstSet({TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'), TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'), TGeogPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')})
    """

    ComponentClass = TGeogPointInst


class TGeomPointSeq(TPointSeq, TGeomPoint):
    """
    Class for representing temporal geometric points of sequence duration.

    ``TGeomPointSeq`` objects can be created with a single argument of type
    string as in MobilityDB.

        >>> TGeomPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')
        >>> TGeomPointSeq('Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')

    Another possibility is to give the arguments as follows:

    * ``instants`` is the set of composing instants, which can be instances
      of ``str`` or ``TGeogPointInst``,
    * ``lower_inc`` and ``upper_inc`` are instances of ``bool`` specifying
      whether the bounds are inclusive or not,  where by default '`lower_inc``
      is ``True`` and ``upper_inc`` is ``False``,
    * ``srid`` is an integer specifiying the SRID
    * ``interp`` which is either ``'Linear'`` or ``'Stepwise'``, the former
      being the default, and

    Some examples are shown next.

        >>> TGeomPointSeq({'Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01', 'Point(10.0 10.0)@2019-09-03 00:00:00+01'})
        >>> TGeomPointSeq({TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'), TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'), TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')})
        >>> TGeomPointSeq({'Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01', 'Point(10.0 10.0)@2019-09-03 00:00:00+01'}, True, True, None, 'Stepwise')
        >>> TGeomPointSeq({TGeomPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'), TGeomPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'), TGeomPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')}, True, True, None, 'Stepwise')
    """

    ComponentClass = TGeomPointInst


class TGeogPointSeq(TPointSeq, TGeogPoint):
    """
    Class for representing temporal geographic points of sequence duration.

    ``TGeogPointSeq`` objects can be created with a single argument of type
    string as in MobilityDB.

        >>> TGeogPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')
        >>> TGeogPointSeq('Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01, Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')

    Another possibility is to give the arguments as follows:

    * ``instants`` is the set of composing instants, which can be instances
      of ``str`` or ``TGeogPointInst``,
    * ``lower_inc`` and ``upper_inc`` are instances of ``bool`` specifying
      whether the bounds are includive or not,  where by default '`lower_inc``
      is ``True`` and ``upper_inc`` is ``False``, and
    * ``srid`` is an integer specifiying the SRID
    * ``interp`` which is either ``'Linear'`` or ``'Stepwise'``, the former
      being the default.

    Some examples are shown next.

        >>> TGeogPointSeq({'Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01', 'Point(10.0 10.0)@2019-09-03 00:00:00+01'})
        >>> TGeogPointSeq({TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'), TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'), TGeogPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')})
        >>> TGeogPointSeq({'Point(10.0 10.0)@2019-09-01 00:00:00+01', 'Point(20.0 20.0)@2019-09-02 00:00:00+01', 'Point(10.0 10.0)@2019-09-03 00:00:00+01'}, True, True, None, 'Stepwise')
        >>> TGeogPointSeq({TGeogPointInst('Point(10.0 10.0)@2019-09-01 00:00:00+01'), TGeogPointInst('Point(20.0 20.0)@2019-09-02 00:00:00+01'), TGeogPointInst('Point(10.0 10.0)@2019-09-03 00:00:00+01')}, True, True, None, 'Stepwise')

    """

    ComponentClass = TGeogPointInst


class TGeomPointSeqSet(TPointSeqSet, TGeomPoint):
    """
    Class for representing temporal geometric points of sequence duration.

    ``TGeomPointSeqSet`` objects can be created with a single argument of type
    string as in MobilityDB.

        >>> TGeomPointSeqSet('{[Point(10.0 10.0)@2019-09-01 00:00:00+01], [Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]}')
        >>> TGeomPointSeqSet('Interp=Stepwise;{[Point(10.0 10.0)@2019-09-01 00:00:00+01], [Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]}')

    Another possibility is to give the arguments as follows:

    * ``sequences`` is the set of composing sequences, which can be instances
      of ``str`` or ``TGeomPointSeq``,
    * ``srid`` is an integer specifiying the SRID, if will be 0 by default if
      not given.
    * ``interp`` can be ``'Linear'`` or ``'Stepwise'``, the former being
      the default, and

    Some examples are shown next.

        >>> TGeomPointSeqSet({'[Point(10.0 10.0)@2019-09-01 00:00:00+01]', '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'})
        >>> TGeomPointSeqSet({'[Point(10.0 10.0)@2019-09-01 00:00:00+01]', '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'}, None, 'Linear')
        >>> TGeomPointSeqSet({'Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]', 'Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'}, None, 'Stepwise')
        >>> TGeomPointSeqSet({TGeomPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'), TGeomPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')})
        >>> TGeomPointSeqSet({TGeomPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'), TGeomPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')}, None, 'Linear')
        >>> TGeomPointSeqSet({TGeomPointSeq('Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]'), TGeomPointSeq('Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')}, None, 'Stepwise')
    """

    ComponentClass = TGeomPointSeq


class TGeogPointSeqSet(TPointSeqSet, TGeogPoint):
    """
    Class for representing temporal geographic points of sequence duration.

    ``TGeogPointSeqSet`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TGeogPointSeqSet('{[Point(10.0 10.0)@2019-09-01 00:00:00+01], [Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]}')
        >>> TGeogPointSeqSet('Interp=Stepwise;{[Point(10.0 10.0)@2019-09-01 00:00:00+01], [Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]}')

    Another possibility is to give the arguments as follows:

    * ``sequences`` is the set of composing sequences, which can be instances
      of ``str`` or ``TGeogPointSeq``,
    * ``srid`` is an integer specifiying the SRID, if will be 0 by default if
      not given.
    * ``interp`` can be ``'Linear'`` or ``'Stepwise'``, the former being
      the default, and

    Some examples are shown next.

        >>> TGeogPointSeqSet({'[Point(10.0 10.0)@2019-09-01 00:00:00+01]', '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'})
        >>> TGeogPointSeqSet({'[Point(10.0 10.0)@2019-09-01 00:00:00+01]', '[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'}, None, 'Linear')
        >>> TGeogPointSeqSet({'Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]', 'Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]'}, None, 'Stepwise')
        >>> TGeogPointSeqSet({TGeogPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'), TGeogPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')})
        >>> TGeogPointSeqSet({TGeogPointSeq('[Point(10.0 10.0)@2019-09-01 00:00:00+01]'), TGeogPointSeq('[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')}, None, 'Linear')
        >>> TGeogPointSeqSet({TGeogPointSeq('Interp=Stepwise;[Point(10.0 10.0)@2019-09-01 00:00:00+01]'), TGeogPointSeq('Interp=Stepwise;[Point(20.0 20.0)@2019-09-02 00:00:00+01, Point(10.0 10.0)@2019-09-03 00:00:00+01]')}, None, 'Stepwise')
    """

    ComponentClass = TGeogPointSeq
