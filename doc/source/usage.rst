Basic usage
===========

``python-mobilitydb`` is a Python converter to and from the `MobilityDB <https://docs.mobilitydb.com/nightly/>`_ temporal types, that is ``tbool``, ``tint``, ``tfloat``, ``ttext``, ``tgeompoint``,  and ``tgeogpoint``.

``TGeomPoint`` and ``TGeogPoint``
---------------------------------

Class :class:`TGeomPoint <mobilitydb.main.TGeomPoint>` represents temporal geometric points with Cartesian (planar) coordinates while :class:`TGeogPoint <mobilitydb.main.TGeogPoint>` represents geographic points with geodetic (spherical) coordinates. We illustrate next how to create instances of the ``TGeomPoint`` class, the creation of instances of the ``TGeogPoint`` class is similar.


New :class:`TGeomPoint <mobilitydb.main.TGeomPoint>` instances can be created by using one of its subclasses :class:`TGeomPointInst <mobilitydb.main.TGeomPointInst>`, :class:`TGeomPointI <mobilitydb.main.TGeomPointI>`, :class:`TGeomPointSeq <mobilitydb.main.TGeomPointI>`, or :class:`TGeomPointS <mobilitydb.main.TGeomPointS>`.

New :class:`TGeomPointInst <mobilitydb.main.TGeomPointInst>` instances can be created either with a single string argument as in MobilityDB or with several arguments: the value, the timestamp, and the SRID, the latter being optional.
In both cases, the value of the point can be specified using a `Well-Known Text (WKT) <https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry>`_ or `Well-Known Binary (WKB) <https://en.wikipedia.org/wiki/Well-known_text#Well-known_binary>`_ representation as well as its `format variations <https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry#Format_variations>`_ Extended Well-Known Text (EWKT) and Extended Well-Known Binary (EWKB).

.. code-block:: python

    >>> from mobilitydb import TGeomPointInst
    >>> TGeomPointInst("POINT(1 1)@2020-01-01 00:00:00+01")
    >>> TGeomPointInst("SRID=4326;POINT(1 1)@2020-01-01 00:00:00+01")
    >>> TGeomPointInst("01010000000000000000004AC00000000000000000@2020-01-01")
    >>> TGeomPointInst("POINT(1 1)", "2020-01-01 00:00:00+01", srid=4326)

New :class:`TGeomPointI <mobilitydb.main.TGeomPointI>` instances can be created either with a single string argument as in MobilityDB or with two arguments: the list of composing instants and the SRID, the latter being optional.

.. code-block:: python

    >>> from mobilitydb import TGeomPointI
    >>> TGeomPointI("{POINT(1 1)@2020-01-01, POINT(2 2)@2020-01-02}")
    >>> TGeomPointI(["POINT(1 1)@2020-01-01", "POINT(2 2)@2020-01-02"], srid=4326)

New :class:`TGeomPointSeq <mobilitydb.main.TGeomPointSeq>` instances can be created either with a single string argument as in MobilityDB or with several arguments: the list of composing instants, the left inclusion flag, the right inclusion flag, the interpolation, and the SRID, where only the first argument is mandatory.

.. code-block:: python

    >>> from mobilitydb import TGeomPointSeq
    >>> TGeomPointSeq("[POINT(1 1)@2020-01-01, POINT(2 2)@2020-01-02]")
    >>> TGeomPointSeq("SRID=4326;[POINT(1 1)@2020-01-01, POINT(2 2)@2020-01-02]")
    >>> TGeomPointSeq(["POINT(1 1)@2020-01-01", "POINT(2 2)@2020-01-02"], lower_inc= True, upper_inc=True, interp='Stepwise', srid=4326)

Finally, new :class:`TGeomPointS <mobilitydb.main.TGeomPointS>` instances can be created either with a single string argument as in MobilityDB or with several arguments: the list of composing sequences, the interpolation, and the SRID, where only the first argument is mandatory.

.. code-block:: python

    >>> from mobilitydb import TGeomPointS
    >>> TGeomPointS("{[POINT(1 1)@2020-01-01, POINT(2 2)@2020-01-02], [POINT(2 2)@2020-01-03, POINT(1 1)@2020-01-04]}")
    >>> TGeomPointS("SRID=4326;{[POINT(1 1)@2020-01-01, POINT(2 2)@2020-01-02], [POINT(2 2)@2020-01-03, POINT(1 1)@2020-01-04]}")
    >>> TGeomPointS(["[POINT(1 1)@2020-01-01, POINT(2 2)@2020-01-02]", "[POINT(2 2)@2020-01-03, POINT(1 1)@2020-01-04]"], interp='Stepwise', srid=4326)


