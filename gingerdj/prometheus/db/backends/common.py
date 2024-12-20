from gingerdj import VERSION


def get_postgres_cursor_class():
    if VERSION < (4, 2):
        from psycopg2.extensions import cursor as cursor_cls
    else:
        from gingerdj.db.backends.postgresql.base import Cursor as cursor_cls
    return cursor_cls
