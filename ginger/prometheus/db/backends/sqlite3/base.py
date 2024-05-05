from ginger.db.backends.sqlite3 import base

from prometheus.db.common import DatabaseWrapperMixin


class DatabaseFeatures(base.DatabaseFeatures):
    """Our database has the exact same features as the base one."""

    pass


class DatabaseWrapper(DatabaseWrapperMixin, base.DatabaseWrapper):
    CURSOR_CLASS = base.SQLiteCursorWrapper
