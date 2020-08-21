Basic usage
===========

``python-mobilitydb`` is a Python converter to and from the temporal types provided by `MobilityDB <https://github.com/MobilityDB/MobilityDB>`_, that is ``tbool``, ``tint``, ``tfloat``, ``ttext``, ``tgeompoint``,  and ``tgeogpoint``.

``TBool``, ``TInt``, and ``TText``
----------------------------------

Classes :class:`TBool <mobilitydb.main.TBool>`, :class:`TInt <mobilitydb.main.TInt>`, and :class:`TText <mobilitydb.main.TInt>` represent, respectively, temporal Booleans, temporal integers, and temporal strings. These classes have in common that their base type is discrete. As a consequence of this, the interpolation for the instances of sequence or sequence set duration is stepwise. We illustrate next how to create new instances of the ``TInt`` class, the creation of instances of the ``TBool`` and ``TText`` classes is similar.

New :class:`TInt <mobilitydb.main.TInt>` instances can be created by using one of its subclasses :class:`TIntInst <mobilitydb.main.TIntInst>`, :class:`TIntInstSet <mobilitydb.main.TIntInstSet>`, :class:`TIntSeq <mobilitydb.main.TIntInstSet>`, or :class:`TIntSeqSet <mobilitydb.main.TIntSeqSet>`.

New :class:`TIntInst <mobilitydb.main.TIntInst>` instances can be created either with a single string argument as in MobilityDB or with two arguments: the value and the timestamp.

.. code-block:: python

    >>> from dateutil.parser import parse
    >>> from mobilitydb import TIntInst
    >>> TIntInst("1@2020-01-01 00:00:00+01")
    >>> TIntInst("1", "2020-01-01 00:00:00+01")
    >>> TIntInst(1, parse("2020-01-01 00:00:00+01"))

New :class:`TIntInstSet <mobilitydb.main.TIntInstSet>` instances can be created either with a single string argument as in MobilityDB or with a tuple or list of the composing instants.

.. code-block:: python

    >>> from mobilitydb import TIntInstSet
    >>> TIntInstSet("{1@2020-01-01, 2@2020-01-02}")
    >>> TIntInstSet(["1@2020-01-01", "2@2020-01-02"])
    >>> TIntInstSet("1@2020-01-01", "2@2020-01-02")
    >>> TIntInstSet(TIntInst(1, "2020-01-01"), TIntInst(2, "2020-01-02"))

New :class:`TIntSeq <mobilitydb.main.TIntSeq>` instances can be created either with a single string argument as in MobilityDB or with several arguments: the list of composing instants, the left inclusion flag, and the right inclusion flag, where only the first argument is mandatory.

.. code-block:: python

    >>> from mobilitydb import TIntSeq
    >>> TIntSeq("[1@2020-01-01, 2@2020-01-02]")
    >>> TIntSeq(["1@2020-01-01", "2@2020-01-02"], lower_inc= True, upper_inc=True)
    >>> TIntSeq([TIntInst(1, "2020-01-01"), TIntInst(2, "2020-01-02")], lower_inc= True, upper_inc=True)

Finally, new :class:`TIntSeqSet <mobilitydb.main.TIntSeqSet>` instances can be created either with a single string argument as in MobilityDB or with a single argument: the list of composing sequences.

.. code-block:: python

    >>> from mobilitydb import TIntSeqSet
    >>> TIntSeqSet("{[1@2020-01-01, 2@2020-01-02], [2@2020-01-03, 1@2020-01-04]}")
    >>> TIntSeqSet(["[1@2020-01-01, 2@2020-01-02]", "[2@2020-01-03, 1@2020-01-04]"])
    >>> TIntSeqSet([TIntSeq("[1@2020-01-01, 2@2020-01-02]"), TIntSeq("[2@2020-01-03, 1@2020-01-04]")])

``TFloat``
----------

Class :class:`TFloat <mobilitydb.main.TFloat>` represents temporal floats. Since the base type of ``TFloat`` is continuous, the interpolation for instances of the sequence or sequence set duration may be either linear or stepwise, the former being the default.

New :class:`TFloat <mobilitydb.main.TFloat>` instances can be created by using one of its subclasses :class:`TFloatInst <mobilitydb.main.TFloatInst>`, :class:`TFloatInstSet <mobilitydb.main.TFloatInstSet>`, :class:`TFloatSeq <mobilitydb.main.TFloatInstSet>`, or :class:`TFloatSeqSet <mobilitydb.main.TFloatSeqSet>`.

New :class:`TFloatInst <mobilitydb.main.TFloatInst>` instances can be created either with a single string argument as in MobilityDB or with two arguments: the value and the timestamp.

.. code-block:: python

    >>> from dateutil.parser import parse
    >>> from mobilitydb import TFloatInst
    >>> TFloatInst("1.0@2020-01-01 00:00:00+01")
    >>> TFloatInst("1.0", "2020-01-01 00:00:00+01")
    >>> TFloatInst(1.0, parse("2020-01-01 00:00:00+01"))

New :class:`TFloatInstSet <mobilitydb.main.TFloatInstSet>` instances can be created either with a single string argument as in MobilityDB or with a tuple or list of the composing instants.

.. code-block:: python

    >>> from mobilitydb import TFloatInstSet
    >>> TFloatInstSet("{1.0@2020-01-01, 2.0@2020-01-02}")
    >>> TFloatInstSet(["1.0@2020-01-01", "2.0@2020-01-02"])
    >>> TFloatInstSet("1.0@2020-01-01", "2.0@2020-01-02")
    >>> TFloatInstSet(TFloatInst("1.0@2020-01-01"), TFloatInst("2.0@2020-01-02"))

New :class:`TFloatSeq <mobilitydb.main.TFloatSeq>` instances can be created either with a single string argument as in MobilityDB or with several arguments: the list of composing instants, the left inclusion flag, the right inclusion flag, and the interpolation, where only the first argument is mandatory.

.. code-block:: python

    >>> from mobilitydb import TFloatSeq
    >>> TFloatSeq("[1.0@2020-01-01, 2.0@2020-01-02]")
    >>> TFloatSeq("Interp=Stepwise;[1.0@2020-01-01, 2.0@2020-01-02]")
    >>> TFloatSeq(["1.0@2020-01-01", "2.0@2020-01-02"], lower_inc= True, upper_inc=True, interp='Stepwise')

Finally, new :class:`TFloatSeqSet <mobilitydb.main.TFloatSeqSet>` instances can be created either with a single string argument as in MobilityDB or with two arguments: the list of composing sequences and the interpolation, where only the first argument is mandatory.

.. code-block:: python

    >>> from mobilitydb import TFloatSeqSet
    >>> TFloatSeqSet("{[1.0@2020-01-01, 2.0@2020-01-02], [2.0@2020-01-03, 1.0@2020-01-04]}")
    >>> TFloatSeqSet(["[1.0@2020-01-01, 2.0@2020-01-02]", "[2.0@2020-01-03, 1.0@2020-01-04]"], interp='Stepwise')

``TGeomPoint`` and ``TGeogPoint``
---------------------------------

Class :class:`TGeomPoint <mobilitydb.main.TGeomPoint>` represents temporal geometric points with Cartesian (planar) coordinates while :class:`TGeogPoint <mobilitydb.main.TGeogPoint>` represents geographic points with geodetic (spherical) coordinates. Since the base type of these classes is continuous, the interpolation for the instances of sequence or sequence set duration may be either linear or stepwise, the former being the default. We illustrate next how to create instances of the ``TGeomPoint`` class, the creation of instances of the ``TGeogPoint`` class is similar.


New :class:`TGeomPoint <mobilitydb.main.TGeomPoint>` instances can be created by using one of its subclasses :class:`TGeomPointInst <mobilitydb.main.TGeomPointInst>`, :class:`TGeomPointInstSet <mobilitydb.main.TGeomPointInstSet>`, :class:`TGeomPointSeq <mobilitydb.main.TGeomPointInstSet>`, or :class:`TGeomPointSeqSet <mobilitydb.main.TGeomPointSeqSet>`.

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

New :class:`TGeomPointInstSet <mobilitydb.main.TGeomPointInstSet>` instances can be created either with a single string argument as in MobilityDB or with two arguments: the list of composing instants and the SRID, the latter being optional.

.. code-block:: python

    >>> from mobilitydb import TGeomPointInstSet
    >>> TGeomPointInstSet("{POINT(1 1)@2020-01-01, POINT(2 2)@2020-01-02}")
    >>> TGeomPointInstSet(["POINT(1 1)@2020-01-01", "POINT(2 2)@2020-01-02"], srid=4326)
    >>> TGeomPointInstSet([TGeomPointInst("POINT(1 1)@2020-01-01"), TGeomPointInst("POINT(2 2)@2020-01-02")], srid=4326)

New :class:`TGeomPointSeq <mobilitydb.main.TGeomPointSeq>` instances can be created either with a single string argument as in MobilityDB or with several arguments: the list of composing instants, the left inclusion flag, the right inclusion flag, the interpolation, and the SRID, where only the first argument is mandatory.

.. code-block:: python

    >>> from mobilitydb import TGeomPointSeq
    >>> TGeomPointSeq("[POINT(1 1)@2020-01-01, POINT(2 2)@2020-01-02]")
    >>> TGeomPointSeq("SRID=4326;[POINT(1 1)@2020-01-01, POINT(2 2)@2020-01-02]")
    >>> TGeomPointSeq("SRID=4326,Interp=Stepwise;[POINT(1 1)@2020-01-01, POINT(2 2)@2020-01-02]")
    >>> TGeomPointSeq(["POINT(1 1)@2020-01-01", "POINT(2 2)@2020-01-02"], lower_inc= True, upper_inc=True, interp='Stepwise', srid=4326)
    >>> TGeomPointSeq([TGeomPointInst("POINT(1 1)@2020-01-01"), TGeomPointInst("POINT(2 2)@2020-01-02")], lower_inc= True, upper_inc=True, interp='Stepwise', srid=4326)

Finally, new :class:`TGeomPointSeqSet <mobilitydb.main.TGeomPointSeqSet>` instances can be created either with a single string argument as in MobilityDB or with several arguments: the list of composing sequences, the interpolation, and the SRID, where only the first argument is mandatory.

.. code-block:: python

    >>> from mobilitydb import TGeomPointSeqSet
    >>> TGeomPointSeqSet("{[POINT(1 1)@2020-01-01, POINT(2 2)@2020-01-02], [POINT(2 2)@2020-01-03, POINT(1 1)@2020-01-04]}")
    >>> TGeomPointSeqSet("SRID=4326;{[POINT(1 1)@2020-01-01, POINT(2 2)@2020-01-02], [POINT(2 2)@2020-01-03, POINT(1 1)@2020-01-04]}")
    >>> TGeomPointSeqSet(["[POINT(1 1)@2020-01-01, POINT(2 2)@2020-01-02]", "[POINT(2 2)@2020-01-03, POINT(1 1)@2020-01-04]"], interp='Stepwise', srid=4326)
    >>> TGeomPointSeqSet([TGeomPointSeq("[POINT(1 1)@2020-01-01, POINT(2 2)@2020-01-02]"), TGeomPointSeq("[POINT(2 2)@2020-01-03, POINT(1 1)@2020-01-04]")], interp='Stepwise', srid=4326)


