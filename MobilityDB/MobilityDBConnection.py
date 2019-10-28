from psycopg2 import extensions
from MobilityDB import *


def MobilityDBRegister(connection):
    if isinstance(connection, extensions.cursor):
        # Retrocompat.
        cursor = connection
    else:
        cursor = connection.cursor()

    # Add MobilityDB types to PostgreSQL adapter and specify the reader function for each type.

    cursor.execute("SELECT NULL::TGEOMPOINT")
    oid = cursor.description[0][1]
    extensions.register_type(extensions.new_type((oid, ), "TGEOMPOINT", TGEOMPOINT.read_from_cursor))

