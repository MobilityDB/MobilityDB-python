import psycopg2
from psycopg2 import extensions
from MobilityDB import *


# Suggestion is to have our own connection method to register our types without asking the user to do this step
class MobilityDB:
    @classmethod
    def connect(cls, host_, database_, user_, password_):
        conn = psycopg2.connect(host=host_, database=database_, user=user_, password=password_)
        MobilityDBRegister(conn)
        return conn


def MobilityDBRegister(connection):
    if isinstance(connection, extensions.cursor):
        # Retrocompat.
        cursor = connection
    else:
        cursor = connection.cursor()

    # Add MobilityDB types to PostgreSQL adapter and specify the reader function for each type.

    cursor.execute("SELECT NULL::TGEOMPOINT")
    oid = cursor.description[0][1]
    extensions.register_type(extensions.new_type((oid,), "TGEOMPOINT", TGEOMPOINT.read_from_cursor))

    cursor.execute("SELECT NULL::TGEOGPOINT")
    oid = cursor.description[0][1]
    extensions.register_type(extensions.new_type((oid,), "TGEOGPOINT", TGEOGPOINT.read_from_cursor))

    cursor.execute("SELECT NULL::TINT")
    oid = cursor.description[0][1]
    extensions.register_type(extensions.new_type((oid,), "TINT", TINT.read_from_cursor))

    cursor.execute("SELECT NULL::TFLOAT")
    oid = cursor.description[0][1]
    extensions.register_type(extensions.new_type((oid,), "TFLOAT", TFLOAT.read_from_cursor))

    cursor.execute("SELECT NULL::TBOOL")
    oid = cursor.description[0][1]
    extensions.register_type(extensions.new_type((oid,), "TBOOL", TBOOL.read_from_cursor))

    cursor.execute("SELECT NULL::TTEXT")
    oid = cursor.description[0][1]
    extensions.register_type(extensions.new_type((oid,), "TTEXT", TTEXT.read_from_cursor))

    cursor.execute("SELECT NULL::TBOX")
    oid = cursor.description[0][1]
    extensions.register_type(extensions.new_type((oid,), "TBOX", TBOX.read_from_cursor))
