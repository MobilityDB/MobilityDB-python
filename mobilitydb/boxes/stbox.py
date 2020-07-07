from dateutil.parser import parse
import warnings

from pymeos.box import STBox as MEOSSTBox

try:
    # Do not make psycopg2 a requirement.
    from psycopg2.extensions import ISQLQuote
except ImportError:
    warnings.warn('psycopg2 not installed', ImportWarning)


class STBox(MEOSSTBox):
    """
    Class for representing bounding boxes composed of coordinate and/or time
    dimensions, where the coordinates may be in 2D (``X`` and ``Y``) or in 3D
    (``X``, ``Y``, and ``Z``). For each dimension, minimum and maximum values
    are stored. The coordinates may be either Cartesian (planar) or geodetic
    (spherical).


    ``STBox`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> "STBOX ((1.0, 2.0), (1.0, 2.0))",
        >>> "STBOX Z((1.0, 2.0, 3.0), (1.0, 2.0, 3.0))",
        >>> "STBOX T((1.0, 2.0, 2001-01-03 00:00:00+01), (1.0, 2.0, 2001-01-03 00:00:00+01))",
        >>> "STBOX ZT((1.0, 2.0, 3.0, 2001-01-04 00:00:00+01), (1.0, 2.0, 3.0, 2001-01-04 00:00:00+01))",
        >>> "STBOX T(, 2001-01-03 00:00:00+01), (, 2001-01-03 00:00:00+01))",
        >>> "GEODSTBOX((1.0, 2.0, 3.0), (1.0, 2.0, 3.0))",
        >>> "GEODSTBOX T((1.0, 2.0, 3.0, 2001-01-03 00:00:00+01), (1.0, 2.0, 3.0, 2001-01-04 00:00:00+01))",
        >>> "GEODSTBOX T((, 2001-01-03 00:00:00+01), (, 2001-01-03 00:00:00+01))",

    Another possibility is to give the bounds in the following order:
    ``xmin``, ``ymin``, ``zmin``, ``tmin``, ``xmax``, ``ymax``, ``zmax``,
    ``tmax``, where the bounds can be instances of ``str``, ``float``
    and ``datetime``. All arguments are optional but they must be given
    in pairs for each dimension and at least one pair must be given.
    When three pairs are given, by default, the third pair will be
    interpreted as representing the ``Z`` dimension unless the ``dimt``
    parameter is given. Finally, the ``geodetic`` parameter determines
    whether the coordinates in the bounds are planar or spherical.

        >>> STBox((1.0, 2.0, 1.0, 2.0))
        >>> STBox((1.0, 2.0, 3.0, 1.0, 2.0, 3.0))
        >>> STBox((1.0, 2.0, '2001-01-03', 1.0, 2.0, '2001-01-03'), dimt=True)
        >>> STBox((1.0, 2.0, 3.0, '2001-01-04', 1.0, 2.0, 3.0, '2001-01-04'))
        >>> STBox(('2001-01-03', '2001-01-03'))
        >>> STBox((1.0, 2.0, 3.0, 1.0, 2.0, 3.0), geodetic=True)
        >>> STBox((1.0, 2.0, 3.0, '2001-01-04', 1.0, 2.0, 3.0, '2001-01-03'), geodetic=True)
        >>> STBox(('2001-01-03', '2001-01-03'), geodetic=True)

    """

    def __init__(self, bounds, dimt=None, srid=None, geodetic=None):
        kwargs = {}

        if srid is not None:
            assert(isinstance(srid, int)), "ERROR: SRID parameter must be Integer"
            kwargs['srid'] = srid
        if geodetic is not None:
            assert(isinstance(geodetic, bool)), "ERROR: Geodetic parameter must be Boolean"
            kwargs['geodetic'] = geodetic

        if isinstance(bounds, str):
            super().__init__(bounds)
        else:
            if geodetic is not None:
                super().__init__(*bounds, **kwargs)
            else:
                super().__init__(*bounds, **kwargs)

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        return STBox(value)

    @staticmethod
    def write(value):
        if not isinstance(value, STBox):
            raise ValueError('Value must be an instance of STBox class')
        return value.__str__()

    # Psycopg2 interface.
    def __conform__(self, protocol):
        if protocol is ISQLQuote:
            return self

    def getquoted(self):
        return "'{}'".format(self.__str__())
    # End Psycopg2 interface.

    def __repr__(self):
        return (f'{self.__class__.__name__ }'
                f'({self.xmin!r}, {self.ymin!r}, {self.zmin!r}, {self.tmin!r}, '
                f'{self.xmax!r}, {self.ymax!r}, {self.zmax!r}, {self.tmax!r}, {self.srid!r}, {self.geodetic!r})')
