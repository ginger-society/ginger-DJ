from gingerdj.contrib.gis.db.backends.base.adapter import WKTAdapter
from gingerdj.db.backends.sqlite3.base import Database


class SpatiaLiteAdapter(WKTAdapter):
    "SQLite adapter for geometry objects."

    def __conform__(self, protocol):
        if protocol is Database.PrepareProtocol:
            return str(self)
