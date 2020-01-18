Basic usage
===========

``python-mobilitydb`` is a Python converter to and from the temporal types provided by `MobilityDB <https://docs.mobilitydb.com/nightly/>`_, that is ``tbool``, ``tint``, ``tfloat``, ``ttext``, ``tgeompoint``,  and ``tgeogpoint``.

``TBool``, ``TInt``, ``TText``,
---------------------------------

Classes :class:`TBool <mobilitydb.main.TBool>`, :class:`TInt <mobilitydb.main.TInt>`, and :class:`TText <mobilitydb.main.TInt>` represent, respectively, temporal Booleans, temporal integers, and temporal strings. These classes have in common that their base type is discrete. As a consequence of this, their interpolation for the sequence and sequence set duration is stepwise. We illustrate next how to create new instances of the ``TInt`` class, the creation of instances of the ``TBool`` and ``TText`` classes is similar.

New :class:`TInt <mobilitydb.main.TInt>` instances can be created by using one of its subclasses :class:`TIntInst <mobilitydb.main.TIntInst>`, :class:`TIntI <mobilitydb.main.TIntI>`, :class:`TIntSeq <mobilitydb.main.TIntI>`, or :class:`TIntS <mobilitydb.main.TIntS>`.

New :class:`TIntInst <mobilitydb.main.TIntInst>` instances can be created either with a single string argument as in MobilityDB or with two arguments: the value and the timestamp.

.. code-block:: python

    >>> from dateutil.parser import parse
    >>> from mobilitydb import TIntInst
    >>> TIntInst("1@2020-01-01 00:00:00+01")
    >>> TIntInst("1", "2020-01-01 00:00:00+01")
    >>> TIntInst(1, parse("2020-01-01 00:00:00+01"))

New :class:`TIntI <mobilitydb.main.TIntI>` instances can be created either with a single string argument as in MobilityDB or with a tuple or list of the composing instants.

.. code-block:: python

    >>> from mobilitydb import TIntI
    >>> TIntI("{1@2020-01-01, 2@2020-01-02}")
    >>> TIntI(["1@2020-01-01", "2@2020-01-02"])
    >>> TIntI("1@2020-01-01", "2@2020-01-02")
    >>> TIntI(TIntInst(1, "2020-01-01"), TIntInst(2, "2020-01-02"))

New :class:`TIntSeq <mobilitydb.main.TIntSeq>` instances can be created either with a single string argument as in MobilityDB or with several arguments: the list of composing instants, the left inclusion flag, and the right inclusion flag, where only the first argument is mandatory.

.. code-block:: python

    >>> from mobilitydb import TIntSeq
    >>> TIntSeq("[1@2020-01-01, 2@2020-01-02]")
    >>> TIntSeq(["1@2020-01-01", "2@2020-01-02"], lower_inc= True, upper_inc=True)
    >>> TIntSeq([TIntInst(1, "2020-01-01"), TIntInst(2, "2020-01-02")], lower_inc= True, upper_inc=True)

Finally, new :class:`TIntS <mobilitydb.main.TIntS>` instances can be created either with a single string argument as in MobilityDB or with a single argument: the list of composing sequences.

.. code-block:: python

    >>> from mobilitydb import TIntS
    >>> TIntS("{[1@2020-01-01, 2@2020-01-02], [2@2020-01-03, 1@2020-01-04]}")
    >>> TIntS(["[1@2020-01-01, 2@2020-01-02]", "[2@2020-01-03, 1@2020-01-04]"])
    >>> TIntS([TIntSeq("[1@2020-01-01, 2@2020-01-02]"), TIntSeq("[2@2020-01-03, 1@2020-01-04]")])

``TFloat``
----------

Class :class:`TFloat <mobilitydb.main.TFloat>` represents temporal floats. New :class:`TFloat <mobilitydb.main.TFloat>` instances can be created by using one of its subclasses :class:`TFloatInst <mobilitydb.main.TFloatInst>`, :class:`TFloatI <mobilitydb.main.TFloatI>`, :class:`TFloatSeq <mobilitydb.main.TFloatI>`, or :class:`TFloatS <mobilitydb.main.TFloatS>`.

New :class:`TFloatInst <mobilitydb.main.TFloatInst>` instances can be created either with a single string argument as in MobilityDB or with two arguments: the value and the timestamp.

.. code-block:: python

    >>> from dateutil.parser import parse
    >>> from mobilitydb import TFloatInst
    >>> TFloatInst("1.0@2020-01-01 00:00:00+01")
    >>> TFloatInst("1.0", "2020-01-01 00:00:00+01")
    >>> TFloatInst(1.0, parse("2020-01-01 00:00:00+01"))

New :class:`TFloatI <mobilitydb.main.TFloatI>` instances can be created either with a single string argument as in MobilityDB or with a tuple or list of the composing instants.

.. code-block:: python

    >>> from mobilitydb import TFloatI
    >>> TFloatI("{1.0@2020-01-01, 2.0@2020-01-02}")
    >>> TFloatI(["1.0@2020-01-01", "2.0@2020-01-02"])
    >>> TFloatI("1.0@2020-01-01", "2.0@2020-01-02")
    >>> TFloatI(TFloatInst("1.0@2020-01-01"), TFloatInst("2.0@2020-01-02"))

New :class:`TFloatSeq <mobilitydb.main.TFloatSeq>` instances can be created either with a single string argument as in MobilityDB or with several arguments: the list of composing instants, the left inclusion flag, the right inclusion flag, and the interpolation, where only the first argument is mandatory.

.. code-block:: python

    >>> from mobilitydb import TFloatSeq
    >>> TFloatSeq("[1.0@2020-01-01, 2.0@2020-01-02]")
    >>> TFloatSeq("Interp=Stepwise;[1.0@2020-01-01, 2.0@2020-01-02]")
    >>> TFloatSeq(["1.0@2020-01-01", "2.0@2020-01-02"], lower_inc= True, upper_inc=True, interp='Stepwise')

Finally, new :class:`TFloatS <mobilitydb.main.TFloatS>` instances can be created either with a single string argument as in MobilityDB or with two arguments: the list of composing sequences and the interpolation, where only the first argument is mandatory.

.. code-block:: python

    >>> from mobilitydb import TFloatS
    >>> TFloatS("{[1.0@2020-01-01, 2.0@2020-01-02], [2.0@2020-01-03, 1.0@2020-01-04]}")
    >>> TFloatS(["[1.0@2020-01-01, 2.0@2020-01-02]", "[2.0@2020-01-03, 1.0@2020-01-04]"], interp='Stepwise')

``TGeomPoint`` and ``TGeogPoint``
---------------------------------

Class :class:`TGeomPoint <mobilitydb.main.TGeomPoint>` represents temporal geometric points with Cartesian (planar) coordinates while :class:`TGeogPoint <mobilitydb.main.TGeogPoint>` represents geographic points with geodetic (spherical) coordinates. We illustrate next how to create instances of the ``TGeomPoint`` class, the creation of instances of the ``TGeogPoint`` class is similar.


New :class:`TGeomPoint <mobilitydb.main.TGeomPoint>` instances can be created by using one of its subclasses :class:`TGeomPointInst <mobilitydb.main.TGeomPointInst>`, :class:`TGeomPointI <mobilitydb.main.TGeomPointI>`, :class:`TGeomPointSeq <mobilitydb.main.TGeomPointI>`, or :class:`TGeomPointS <mobilitydb.main.TGeomPointS>`.

New :class:`TGeomPointInst <mobilitydb.main.TGeomPointInst>` instances can be created either with a single string argument as in MobilityDB or with several arguments: the value, the timestamp, and the SRID, the latter being optional.
In both cases, the value of the point can be specified using a `Well-Known Text (WKT) <https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry>`_ or `Well-Known Binary (WKB) <https://en.wikipedia.org/wiki/Well-known_text#Well-known_binary>`_ representation as well as its `format variations <https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry#Format_variations>`_ Extended Well-Known Text (EWKT) and Extended Well-Known Binary (EWKB).

.. code-block:: python

    >>> from dateutil.parser import parse
    >>> from postgis import Point
    >>> from mobilitydb import TGeomPointInst
    >>> TGeomPointInst("POINT(1 1)@2020-01-01 00:00:00+01")
    >>> TGeomPointInst("SRID=4326;POINT(1 1)@2020-01-01 00:00:00+01")
    >>> TGeomPointInst("01010000000000000000004AC00000000000000000@2020-01-01")
    >>> TGeomPointInst("POINT(1 1)", "2020-01-01 00:00:00+01", srid=4326)
    >>> TGeomPointInst(Point(1, 1), parse("2020-01-01 00:00:00+01"), srid=4326)

New :class:`TGeomPointI <mobilitydb.main.TGeomPointI>` instances can be created either with a single string argument as in MobilityDB or with two arguments: the list of composing instants and the SRID, the latter being optional.

.. code-block:: python

    >>> from mobilitydb import TGeomPointI
    >>> TGeomPointI("{POINT(1 1)@2020-01-01, POINT(2 2)@2020-01-02}")
    >>> TGeomPointI(["POINT(1 1)@2020-01-01", "POINT(2 2)@2020-01-02"], srid=4326)
    >>> TGeomPointI([TGeomPointInst("POINT(1 1)@2020-01-01"), TGeomPointInst("POINT(2 2)@2020-01-02")], srid=4326)

New :class:`TGeomPointSeq <mobilitydb.main.TGeomPointSeq>` instances can be created either with a single string argument as in MobilityDB or with several arguments: the list of composing instants, the left inclusion flag, the right inclusion flag, the interpolation, and the SRID, where only the first argument is mandatory.

.. code-block:: python

    >>> from mobilitydb import TGeomPointSeq
    >>> TGeomPointSeq("[POINT(1 1)@2020-01-01, POINT(2 2)@2020-01-02]")
    >>> TGeomPointSeq("SRID=4326;[POINT(1 1)@2020-01-01, POINT(2 2)@2020-01-02]")
    >>> TGeomPointSeq("SRID=4326,Interp=Stepwise;[POINT(1 1)@2020-01-01, POINT(2 2)@2020-01-02]")
    >>> TGeomPointSeq(["POINT(1 1)@2020-01-01", "POINT(2 2)@2020-01-02"], lower_inc= True, upper_inc=True, interp='Stepwise', srid=4326)
    >>> TGeomPointSeq([TGeomPointInst("POINT(1 1)@2020-01-01"), TGeomPointInst("POINT(2 2)@2020-01-02")], lower_inc= True, upper_inc=True, interp='Stepwise', srid=4326)

Finally, new :class:`TGeomPointS <mobilitydb.main.TGeomPointS>` instances can be created either with a single string argument as in MobilityDB or with several arguments: the list of composing sequences, the interpolation, and the SRID, where only the first argument is mandatory.

.. code-block:: python

    >>> from mobilitydb import TGeomPointS
    >>> TGeomPointS("{[POINT(1 1)@2020-01-01, POINT(2 2)@2020-01-02], [POINT(2 2)@2020-01-03, POINT(1 1)@2020-01-04]}")
    >>> TGeomPointS("SRID=4326;{[POINT(1 1)@2020-01-01, POINT(2 2)@2020-01-02], [POINT(2 2)@2020-01-03, POINT(1 1)@2020-01-04]}")
    >>> TGeomPointS(["[POINT(1 1)@2020-01-01, POINT(2 2)@2020-01-02]", "[POINT(2 2)@2020-01-03, POINT(1 1)@2020-01-04]"], interp='Stepwise', srid=4326)
    >>> TGeomPointS([TGeomPointSeq("[POINT(1 1)@2020-01-01, POINT(2 2)@2020-01-02]"), TGeomPointSeq("[POINT(2 2)@2020-01-03, POINT(1 1)@2020-01-04]")], interp='Stepwise', srid=4326)


