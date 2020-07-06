from dateutil.parser import parse
import warnings

from pymeos.box import TBox as MEOSTBox

try:
    # Do not make psycopg2 a requirement.
    from psycopg2.extensions import ISQLQuote
except ImportError:
    warnings.warn('psycopg2 not installed', ImportWarning)


class TBox(MEOSTBox):
    """
    Class for representing bounding boxes with value (``X``) and/or time (``T``)
    dimensions.


    ``TBox`` objects can be created with a single argument of type string
    as in MobilityDB.

        >>> TBox("TBOX((1.0, 2000-01-01), (2.0, 2000-01-02))")
        >>> TBox("TBOX((1.0,), (2.0,))")
        >>> TBox("TBOX((, 2000-01-01), (, 2000-01-02))")

    Another possibility is to give the bounds in the following order:
    ``xmin``, ``tmin``, ``xmax``, ``tmax``, where the bounds can be
    instances of ``str``, ``float`` or ``datetime``. All arguments are
    optional but they must be given in pairs for each dimension and at
    least one pair must be given.

        >>> TBox("1.0", "2000-01-01", "2.0", "2000-01-02")
        >>> TBox(1.0, 2.0)
        >>> TBox(parse("2000-01-01"), parse("2000-01-02"))

    """

    def __init__(self, *args, **kwargs):
        # Two string arguments given - this construction is not supported by MEOSTBox
        if len(args) == 2 and all(isinstance(arg, str) for arg in args):
            try:
                args = [float(arg) for arg in args]
            except:
                args = [parse(arg) for arg in args]
        super().__init__(*args, **kwargs)

    @staticmethod
    def read_from_cursor(value, cursor=None):
        if not value:
            return None
        return TBox(value)

    @staticmethod
    def write(value):
        if not isinstance(value, TBox):
            raise ValueError('Value must be an instance of TBox class')
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
                f'({self.xmin!r}, {self.tmin!r}, {self.xmax!r}, {self.tmax!r})')

